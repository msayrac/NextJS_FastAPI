from pydantic import BaseModel
from typing import Optional, List
from fastapi import APIRouter
from sqlalchemy.orm import joinedload
from ..models import Workout, Routine
from ..deps import db_dependency, user_dependency

router = APIRouter(
    prefix="/routines",
    tags=["routines"]
)

class RoutineBase(BaseModel):
    name:str
    description:Optional[str]=None

class RoutineCreate(RoutineBase):
    workouts: List[int] = []

@router.get("/")
def get_routines(db: db_dependency, user:user_dependency):
    return db.query(Routine).options(joinedload(Routine.workouts)).filter(Routine.user_id == user.get('id')).all()

@router.post("/")
def create_routine(db: db_dependency, user:user_dependency,routine:RoutineCreate):
    db_routine = Routine(name = routine.name, description =routine.description, user_id =user.get('id'))

    for workout_id in routine.workouts:
        workout = db.query(Workout).filter(Workout.id == workout_id).first()








