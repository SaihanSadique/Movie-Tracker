from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/demo")

@router.get("/hello-world")
def hello_world():
    pass