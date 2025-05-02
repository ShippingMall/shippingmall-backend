from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import SessionLocal, engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from fastapi import Depends
from sqlalchemy.orm import Session

from app import crud, database, models, schemas
from app.database import SessionLocal, engine


@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    existing_email = crud.get_user_by_email(db, user.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    return crud.create_user(db, user)
