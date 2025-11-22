from fastapi import FastAPI, HTTPException
from database import create_db_and_tables, SessionDep
from models import User, UserLogin, Score, ScoreCreate
from sqlmodel import select

app = FastAPI()

# add CORS

@app.get("/")
async def health_check():
    return {"message": "The API is active."}

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/register/")
def register(user: UserLogin, session: SessionDep):
    existing_user = session.exec(select(User).where(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="username already exists")
    
    new_user = User(username=user.username, password=user.password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@app.post("/login/")
def login(user: UserLogin, session: SessionDep):
    existing_user = session.exec(select(User).where(User.username == user.username)).first()
    if not existing_user or existing_user.password != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"user_id": existing_user.id, "username": existing_user.username}

@app.post("/scores/", response_model=Score)
def submit_score(score_data: ScoreCreate, session: SessionDep):
    score = Score.model_validate(score_data)
    session.add(score)
    session.commit()
    session.refresh(score)
    return score

@app.get("/leaderboard/", response_model=list[Score])
def get_leaderboard(session: SessionDep):
    scores = session.exec(select(Score).order_by(Score.points.desc()).limit(10)).all()
    return scores