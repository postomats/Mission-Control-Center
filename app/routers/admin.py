from fastapi import APIRouter, HTTPException
from ..utilities import change_role, open_all_cells, is_admin
from pydantic import EmailStr

router = APIRouter()


@router.get("/open_all_cells")
def open_all_cells(jwt: str):
    if is_admin(jwt):
        open_all_cells()
    return {"status": True}


@router.put("/new_admin")
def do_new_admin(jwt: str, email: EmailStr):
    response = change_role(jwt=jwt, email=email, role="Admin")
    if response.get("status"):
        return response
    raise HTTPException(
        status_code=response.get("error"), detail=response.get("message")
    )


@router.put("/new_worker")
def do_new_worker(jwt: str, email: EmailStr):
    response = change_role(jwt=jwt, email=email, role="Worker")
    if response.get("status"):
        return response
    raise HTTPException(
        status_code=response.get("error"), detail=response.get("message")
    )
