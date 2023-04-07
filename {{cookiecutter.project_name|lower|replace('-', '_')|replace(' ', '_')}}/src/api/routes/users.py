from fastapi import APIRouter, Depends

from src.api import dependencies
from src.controllers import UserController
from src.models import User
from src.schemas import UserCreateRequest, UserResponse, UserUpdateRequest

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def read_current_user(
    current_user: User = Depends(dependencies.get_current_user),
):
    """Get current user"""
    return current_user


@router.delete("/me", status_code=204)
async def delete_current_user(
    current_user: User = Depends(dependencies.get_current_user),
    controller: UserController = Depends(dependencies.get_controller(UserController)),
):
    """Delete current user"""
    await controller.delete_user_by_id(id=current_user.id)


@router.get("/", response_model=list[UserResponse])
async def get_users(
    controller: UserController = Depends(dependencies.get_controller(UserController)),
):
    """Get all users"""
    users = await controller.get_users()
    return list(users)


@router.get("/{id}", response_model=UserResponse)
async def get_user(
    id: str,
    controller: UserController = Depends(dependencies.get_controller(UserController)),
):
    """Get a user by id"""
    user = await controller.get_user_by_attribute(attribute="id", value=id)
    return user


@router.post("/register", status_code=201, response_model=UserResponse)
async def register_new_user(
    new_user: UserCreateRequest,
    controller: UserController = Depends(dependencies.get_controller(UserController)),
):
    """Create new user"""
    user = await controller.create_user(new_user=new_user)
    return user


@router.delete("/{id}", status_code=204)
async def delete_user(
    id: str,
    controller: UserController = Depends(dependencies.get_controller(UserController)),
    current_user: User = Depends(dependencies.get_current_user),
):
    """Delete a user by id"""
    await controller.delete_user_by_id(id=id)


@router.patch("/{id}", response_model=UserResponse)
async def update_user(
    id: str,
    update_user: UserUpdateRequest,
    controller: UserController = Depends(dependencies.get_controller(UserController)),
    current_user: User = Depends(dependencies.get_current_user),
):
    """Update user data"""
    user = await controller.update_user_by_id(id=id, user_update=update_user)
    return user
