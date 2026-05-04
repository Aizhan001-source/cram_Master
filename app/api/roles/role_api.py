from fastapi import APIRouter, Depends
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from data_access.db.session import get_db
from data_access.roles.role_repository import RoleRepository
from business_logic.roles.role_service import RoleService
from .role_schemas import RoleResponse

router = APIRouter()


@router.get("/", response_model=list[RoleResponse])
async def get_all_roles(
    session: AsyncSession = Depends(get_db)
):
    repo = RoleRepository(session)
    service = RoleService(repo)

    roles = await service.get_all_roles()

    return roles


@router.get("/{role_id}", response_model=RoleResponse)
async def get_role_by_id(
    role_id: UUID,
    session: AsyncSession = Depends(get_db)
):
    repo = RoleRepository(session)
    service = RoleService(repo)

    role = await service.get_role_by_id(role_id)

    return role