from datetime import datetime, timedelta
import json
from fastapi import WebSocket,WebSocketDisconnect,APIRouter,HTTPException,status,Path
from fastapi.responses import HTMLResponse
from app.dependancies.db_dependencies import db_dependancy
from app.services.auth_services import get_current_user_websocket
from ..agents.chat_agent import chat_agent
from ..agents.chat_agent import SupportDependancies
from ..services.chat_services import store_chat_message,retrieve_chat_messages,summarise_daily_nutrition_messages
from ..dependancies.auth_dependancies import user_dependancy
from pydantic_ai.messages import ModelRequest, ModelResponse
from pydantic_ai.messages import UserPromptPart, TextPart
from app.rate_limiter import increment_message_counter
import asyncio

chat_router=APIRouter(prefix="/chat",tags=["chat"])

@chat_router.websocket("/ws")
async def websocket_chat_endpoint(websocket: WebSocket,db:db_dependancy):
    await websocket.accept()
 
    try:
        user = await get_current_user_websocket(websocket, db)
        user_name = user.name
        user_id=user.uuid
        user_is_pro=user.is_pro
                
        init_json= await websocket.receive_json()
        init_dict=init_json
        
        if init_dict["type"]=="init" and "date" in init_dict:
            selected_date_str=init_dict["date"]
            selected_date=datetime.strptime(selected_date_str,"%Y-%m-%d").date()
        else:
            await websocket.close(code=1003)    
           
        messages_for_today=retrieve_chat_messages(db,user_id,selected_date) 
        messages = []
        for item in messages_for_today:
            msg_type = item["sender"]
            msg_content = item["message"]

            if msg_type == "human":
                msg_obj = ModelRequest(parts=[UserPromptPart(content=msg_content)])
            else:
                msg_obj = ModelResponse(parts=[TextPart(content=msg_content)])
            
            messages.append(msg_obj)
          
        async for message in websocket.iter_text():
            try:
                message_data = json.loads(message)

                if message_data.get("type") != "message":
                    raise ValueError("Invalid message type")

                content = message_data["content"]
                timestamp_str = message_data.get("timestamp")
                if not timestamp_str:
                    raise ValueError("Missing timestamp")
                
                timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                
                if not await increment_message_counter(user_id,user_is_pro):
                    await websocket.send_text("Daily message limit reached (5 per day). Try again tomorrow.")
                    await websocket.close(code=1008, reason="Rate limit exceeded")
                    return
                
                store_chat_message(db,user_id,content,sender="user",message_timestamp=timestamp,message_date=selected_date)

                async with chat_agent.run_stream(content, message_history=messages, deps=SupportDependancies(user_name=user_name)) as result:
                    bot_response = await result.get_output()
                    messages.append(ModelRequest(parts=[UserPromptPart(content=message)]))
                    messages.append(ModelResponse(parts=[TextPart(content=bot_response)]))
                    store_chat_message(db,user_id,bot_response,sender="assistant",message_timestamp=timestamp+timedelta(seconds=1),message_date=selected_date)
                    await websocket.send_text(bot_response)
                    asyncio.create_task(summarise_daily_nutrition_messages(db,user_id,selected_date))
                
            except (json.JSONDecodeError, ValueError) as e:
                print(f"WebSocket error: {e}")
                await websocket.close(code=1003, reason=str(e))       
            
    except WebSocketDisconnect:
        print(f"Client {user_name} disconnected")

    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()

@chat_router.get('/history/{date}')
async def get_history_for_date(date:str,db:db_dependancy,user:user_dependancy):
    if not date:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    try:
        selected_date=datetime.strptime(date,"%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid date format")
    
    messages=retrieve_chat_messages(db,user.uuid,selected_date)
    
    return messages
            
@chat_router.get("/chat-ui")
async def get_chat_ui():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Chat</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f2f5;
                display: flex;
                flex-direction: column;
                align-items: center;
                height: 100vh;
                margin: 0;
                padding: 0;
            }
            .chat-container {
                width: 100%;
                max-width: 600px;
                background-color: #fff;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                margin-top: 50px;
                border-radius: 10px;
                overflow: hidden;
                display: flex;
                flex-direction: column;
            }
            .messages {
                flex: 1;
                padding: 20px;
                overflow-y: auto;
                height: 70vh;
            }
            .message {
                margin: 10px 0;
                padding: 10px 15px;
                border-radius: 10px;
                max-width: 80%;
            }
            .user {
                align-self: flex-end;
                background-color: #dcf8c6;
            }
            .ai {
                align-self: flex-start;
                background-color: #ececec;
            }
            .input-container {
                display: flex;
                padding: 10px;
                border-top: 1px solid #ccc;
            }
            input[type="text"] {
                flex: 1;
                padding: 10px;
                border: none;
                outline: none;
                font-size: 16px;
            }
            button {
                padding: 10px 20px;
                border: none;
                background-color: #007bff;
                color: white;
                cursor: pointer;
                font-size: 16px;
            }
            button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <h1>Munchbot</h1>
        <div class="chat-container">
            <div class="messages" id="messages"></div>
            <div class="input-container">
                <input type="text" id="messageInput" placeholder="Ask me anything..." />
                <button onclick="sendMessage()">Send</button>
            </div>
        </div>

        <script>
            const token = localStorage.getItem('access_token');
            if (!token) {
                alert("No token found, please login first!");
            }

            const socket = new WebSocket(`ws://localhost:8000/chat/ws?token=${token}`);

            const messagesDiv = document.getElementById("messages");
            const input = document.getElementById("messageInput");

            socket.onmessage = function(event) {
                addMessage("ai", event.data);
            };

            function sendMessage() {
                const message = input.value;
                if (message.trim() === "") return;

                socket.send(message);
                addMessage("user", message);
                input.value = "";
            }

            function addMessage(sender, text) {
                const messageDiv = document.createElement("div");
                messageDiv.classList.add("message", sender);
                messageDiv.innerText = text;
                messagesDiv.appendChild(messageDiv);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)      