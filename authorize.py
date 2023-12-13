from fastapi_jwt_auth import AuthJWT
from fastapi import  HTTPException, status, Depends



def authorize_user(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
        return Authorize
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail = "Invalid Token")