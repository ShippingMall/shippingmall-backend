from fastapi import FastAPI
from app.routes import shipment

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "ShippingMall Logistics API is live"}

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

# App instance
app = FastAPI()
app.include_router(shipment.router, prefix="/shipments", tags=["Shipments"])
# Secret and config
SECRET_KEY = "shippingmall-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Dummy user (for demo)
fake_user = {"username": "admin", "password": "password"}

# Create access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Verify token
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Routes
@app.get("/")
def read_root():
    return {"message": "🚀 ShippingMall Auth API is running!"}


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if (
        form_data.username != fake_user["username"]
        or form_data.password != fake_user["password"]
    ):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/protected")
def protected_route(user: dict = Depends(verify_token)):
    return {"message": f"Hello, {user['sub']}! You're authenticated."}
