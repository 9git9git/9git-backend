from app.schemas.todo import TodoResponse
from app.schemas.memo import MemoResponse
from app.schemas.base import BaseModel
from typing import List


class TodosAndMemosResponse(BaseModel):
    todos: List[TodoResponse]
    memos: List[MemoResponse]
