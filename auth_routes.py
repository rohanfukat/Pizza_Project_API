from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.exceptions import HTTPException
from database import Session, engine
from schemas import SignUPModel, LoginModel
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder


auth_router = APIRouter(
    prefix="/auth",
    tags = ["Auth"]
)

session = Session(bind = engine)

@auth_router.get("/")
async def hello(Authorize:AuthJWT=Depends()):
    """
    Testing Route for hello world
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid token")
    return {"message": "hello world"}


@auth_router.post("/signup", status_code = status.HTTP_201_CREATED)
async def signup(user : SignUPModel):
    """
    SignUp route requeste body
                username:int
                email:str
                password:str
                is_staff:bool
                is_active:bool   
    """
    db_email = session.query(User).filter(User.email == user.email).first()

    if(db_email is not None):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="User with the email already exists")

    db_username = session.query(User).filter(User.username == user.username).first()

    if(db_username is not None):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="User with the username already exists")
    

    new_user = User(
        username = user.username,
        email = user.email,
        password = generate_password_hash(user.password),
        is_active = user.is_active,
        is_staff = user.is_staff
    )

    session.add(new_user)
    session.commit()
    return jsonable_encoder({new_user})


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login(login_data:LoginModel, Authorize:AuthJWT=Depends()):
    """
                username:str
                password:str
    """
    db_user = session.query(User).filter(User.username == login_data.username).first()
    if db_user and check_password_hash(db_user.password ,login_data.password):
        access_token = Authorize.create_access_token(subject=db_user.username)
        refresh_token = Authorize.create_refresh_token(subject = db_user.username)

        response = {
            "access":access_token,
            "refresh":refresh_token
        }
        return jsonable_encoder(response)
    else:
        return HTTPException(status_code= status.HTTP_400_BAD_REQUEST,
                             detail= "Invalid username or Password")
    
@auth_router.get("/refresh")
async def refresh_token(Authorize:AuthJWT=Depends()):
    """
     This creates a new access token. It requires an refresh token.
     The function automatically fetches the data from the header and performs the authorization
    """
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
        detail = "Please provide a valid refresh token")
    
    current_user = Authorize.get_jwt_subject()
    
    access_token = Authorize.create_access_token(subject = current_user)


    return jsonable_encoder({"access":access_token})
