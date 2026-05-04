from uuid import UUID
from fastapi import HTTPException, status

from data_access.roles.role_repository import RoleRepository
from data_access.db.models.role import Role


class RoleService:
    def __init__(self, repo: RoleRepository):
        self.repo = repo

    async def get_all_roles(self) -> list[Role]:
        roles = await self.repo.get_all()
        return roles

    async def get_role_by_id(self, role_id: UUID) -> Role:
        role = await self.repo.get_by_id(role_id)

        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )

        return role