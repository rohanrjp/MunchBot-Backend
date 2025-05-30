from fastapi import Depends
from ..database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependancy=Annotated[Session,Depends(get_db)]     


 