from src.repository import RepositoryORM
from src.events.models import EventORM 
from sqlalchemy.ext.asyncio import AsyncSession


class EventRepository(RepositoryORM):

    def __init__(self, session: AsyncSession):
        super().__init__(session=session)
        self.model = EventORM