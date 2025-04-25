from fastapi import WebSocket,WebSocketDisconnect,APIRouter
from fastapi.responses import HTMLResponse
from ..agents.chat_agent import chat_agent
from ..dependancies.auth_dependancies import user_dependancy

chat_router=APIRouter(prefix="/chat",tags=["chat"])

@chat_router.websocket("/ws")
async def websocket_chat_endpoint(websocket:WebSocket):
    await websocket.accept()
    try:
        async for message in websocket.iter_text():
            async with chat_agent.run_stream(message,message_history=[]) as result:
                    await websocket.send_text(await result.get_output())
    except WebSocketDisconnect:
        print("client disconnected")
            
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
            const socket = new WebSocket("ws://localhost:8000/chat/ws");

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