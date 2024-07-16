from datetime import datetime,timedelta
from fastapi import HTTPException,status,Security
from dotenv import load_dotenv
import os 
from jose import JWTError,jwt



load_dotenv()
SECRET_KEY = str(os.environ.get("SECRET_KEY"))
ALGORITHM = str(os.environ.get("ALGORITHM"))
def get_token(id):
    payload = {
        "user_id": id,
        "exp": datetime.now() + timedelta(minutes=100),
    }
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    print(type(access_token))
    return access_token




def decode_token_user_id(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token",
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token"

        )
    


def logging_token(u_id,e_mail):
    payload = {
        "u_id" : u_id,
        "e_mail" : e_mail,
        "exp" : datetime.now() + timedelta(minutes=100)
    }
    access_token  = jwt.encode(payload,SECRET_KEY,ALGORITHM)
    print(type(access_token))
    return access_token


def decode_token_u_id(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("u_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token",
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token"

        )



    


def decode_token_user_password(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_password = payload.get("password")
        if not user_password:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token",
            )
        return user_password
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token"

        )
    


#-----------------------------------------------------admin-----------------------------------------


def get_admin_id_token(id):
    payload = {
        "admin_id": id,
        "exp": datetime.utcnow() + timedelta(minutes=100),
    }
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    print(type(access_token))
    return access_token



def  admin_logging_token(a_id,u_name,password):
    payload = {
        "a_id" : a_id,
        "u_name" : u_name,
        "password" : password,
        "exp" : datetime.utcnow() + timedelta(minutes=100)
    }
    access_token  = jwt.encode(payload,SECRET_KEY,ALGORITHM)
    print(type(access_token))
    return access_token




def decode_token_a_id(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        admin_id = payload.get("a_id")
        if not admin_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token",
            )
        return admin_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token"

        )
    


def decode_token_a_name(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        admin_name = payload.get("u_name")
        if not admin_name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token",
            )
        return admin_name
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token"

        )