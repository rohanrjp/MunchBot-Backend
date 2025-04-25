from fastapi import HTTPException,status

Invalid_Credentials_Exception=HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid Credentials",
    headers={"WWW-Authenticate": "Bearer"}
)