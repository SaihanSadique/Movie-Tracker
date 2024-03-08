from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/demo")

@router.get("/")
def hello_world():
    return "hello world"