from fastapi import APIRouter, HTTPException
from ..utilities import change_role, is_admin
from ..utilities import open_all_cells as OPEN_ALL_CELLS
from pydantic import EmailStr

router = APIRouter()


@router.get("/open_all_cells")
def open_all_cells(jwt: str):
    if is_admin(jwt):
        OPEN_ALL_CELLS()
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
