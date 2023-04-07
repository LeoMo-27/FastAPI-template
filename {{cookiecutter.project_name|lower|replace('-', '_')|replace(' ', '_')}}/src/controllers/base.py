from sqlalchemy.ext.asyncio import AsyncSession


class BaseController:
    def __init__(self, session: AsyncSession):
        self.session = session
