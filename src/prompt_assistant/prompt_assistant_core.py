import uvicorn
from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from src.prompt_assistant.prompt_assistant import prompt_suggestion, prompt_remix


router = APIRouter(
    prefix='/prompt_assistant',
    tags=['prompt_assistant']
)

class Query(BaseModel):
    question: str


# 根據提問建議prompt
@router.post("/suggest/")
async def suggest(query: Query):
    try:
        response = prompt_suggestion(query.question)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# 先搜尋其他使用者用過的prompt，再結合這些歷史紀錄與提問，來建議prompt(也就是RAG)
@router.post("/remix/")
def remix(query: Query):
    try:
        response = prompt_remix(query.question)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


