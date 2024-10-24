from fastapi import APIRouter, Depends, HTTPException, Header
from starlette import status
from sqlalchemy.orm import Session
from typing import Optional, Annotated, Tuple, List

from app.database.mysql.crud.auth import get_admin, create_user, get_members
from app.database.mysql.session import get_session, get_read_session
from app.database.mongodb.session import MongoHandler
from app.model.request.auth import UserCreateModel, UserUpdateModel
from app.model.response.auth import UserModel
from app.factory.auth import GradeChecker, get_current_user

router = APIRouter()

@router.post("/signup")
async def signup(
    db: Annotated[Session, Depends(get_session)],
    user: UserCreateModel,
):
    db_user = get_admin(db=db, email=user.email)
    
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email already exists.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    else:
        create_user(user=user, db=db)
    
    return {
        "email": user.email,
        "hashed_password": user.password,
        "name": user.name,
        "phone": user.phone
    }
    
@router.post("/signup/invite")
async def signup_invite(user: AdminCreateModel,
                        db: Annotated[Session, Depends(get_db)],
                        _: Annotated[AdminModel, Depends(GradeChecker(allowed_grade="manager"))]):
    db_user = get_admin(db=db, email=user.email)
    
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email already exists.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    else:
        create_user(user=user, db=db)
    
    return {
        "email": user.email,
        "hashed_password": user.password,
        "name": user.name,
        "phone": user.phone
    }
    
@router.get("/me")
async def get_me(
    user: Annotated[AdminModel, Depends(get_current_user)]
) -> dict:
    return {
        "result": True,
        "data": user
    }

@router.put("/me")
async def update_my_profile(
    user: Annotated[AdminModel, Depends(get_current_user)],
    update_info: AdminUpdateModel,
    db: Annotated[Session, Depends(get_db)],
) -> dict:
    updated_user = update_user(db=db, admin_id=user.id, user=update_info)
    return {
        "result": True,
        "data": updated_user
    }

@router.get("/members")
async def get_member_list(
    user: Annotated[AdminModel, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> dict:
    users = get_members(db=db, enterprise_id=user.enterprise_id, offset=0, limit=100)
    return {
        "result": True,
        "data": users
    }

@router.post("/invite")
async def invite_member(
    user: Annotated[AdminModel, Depends(get_current_user)],
    member: AdminCreateModel,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[AdminModel, Depends(GradeChecker(allowed_grade="manager"))]
):
    pass

@router.delete("/invite")
async def invite_member(
    user: Annotated[AdminModel, Depends(get_current_user)],
    member: AdminCreateModel,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[AdminModel, Depends(GradeChecker(allowed_grade="manager"))]
):
    pass

@router.post("/block/lock")
async def block_member(
    user: Annotated[AdminModel, Depends(get_current_user)],
    member: AdminCreateModel,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[AdminModel, Depends(GradeChecker(allowed_grade="manager"))]
):
    pass

@router.put("/block/unlock")
async def unlock_block(
    user: Annotated[AdminModel, Depends(get_current_user)],
    member: AdminCreateModel,
    db: Annotated[Session, Depends(get_db)],
    _: Annotated[AdminModel, Depends(GradeChecker(allowed_grade="manager"))]
):
    pass