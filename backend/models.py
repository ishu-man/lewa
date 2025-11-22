from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str 

class Score(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    points: int
    accuracy: int
    user_id: int = Field(foreign_key="user.id")
    username: str

class UserLogin(SQLModel):
    username: str
    password: str

class ScoreCreate(SQLModel):
    points: int
    accuracy: int
    user_id: int
    username: str