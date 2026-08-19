from fastapi import APIRouter


router = APIRouter()

@router.get("/home")
def home ():
    return "welcome to home "
