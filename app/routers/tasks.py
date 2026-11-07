from fastapi import APIRouter, Path, status, Depends, HTTPException, Query
from typing import Annotated
from app.models.models import Task
from app.models.query import FilterParams
from sqlalchemy.orm import Session
from app.database import get_session
from app.schemas.task_schemas import TaskCreate, TaskResponse, TaskUpdate
from sqlalchemy import select


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
    )

SessionDep = Annotated[Session, Depends(get_session)]

@router.get("/", response_model=list[TaskResponse])
def get_tasks(session: SessionDep, filter_query: Annotated[FilterParams, Query()]):
    stmt = select(Task)
    sort_columns = {
        "id": Task.id,
        "finished": Task.finished,
        "task_name": Task.task_name
        }

    sort_column = sort_columns[filter_query.sort_by]

    if filter_query.order == "asc":
        stmt = stmt.order_by(sort_column.asc())
    else:
        stmt = stmt.order_by(sort_column.desc())
    
    if filter_query.finished is not None:
        stmt = stmt.where(Task.finished == filter_query.finished)

    stmt = stmt.limit(filter_query.limit).offset(filter_query.offset)

    tasks = session.scalars(stmt).all()

    return [
        TaskResponse(
            id=task.id,
            task_name=task.task_name,
            finished=task.finished
        ) 
        for task in tasks
    ]
                        

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def post_tasks(task_data: TaskCreate, session: SessionDep):
    task = Task(**task_data.model_dump())

    session.add(task)
    session.commit()
    session.refresh(task)

    return TaskResponse(
        id=task.id,
        task_name=task.task_name,
        finished=task.finished
    )

    
@router.get("/{id}", response_model=TaskResponse)
def get_task(id: Annotated[int, Path(gt=0)], session: SessionDep):
    task = session.get(Task, id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="task does not exist"
        )

    return TaskResponse(
        id=task.id,
        task_name=task.task_name,
        finished=task.finished,
    )



@router.patch("/{id}", response_model=TaskResponse)
def patch_task(id: Annotated[int, Path(gt=0)], data: TaskUpdate, session: SessionDep):
    task = session.get(Task, id)

    if task is None:
        raise HTTPException(
                status_code=404,
                detail="Task does not exist"
            )

    update=data.model_dump(exclude_unset=True)

    for column, value in update.items():
        setattr(task, column, value)

    session.commit()
    session.refresh(task)

    return TaskResponse(
            id=task.id,
            task_name=task.task_name,
            finished=task.finished,
        )
    


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: Annotated[int, Path(gt=0)], session: SessionDep):
    task = session.get(Task, id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="task does not exist"
        )

    session.delete(task)
    session.commit()