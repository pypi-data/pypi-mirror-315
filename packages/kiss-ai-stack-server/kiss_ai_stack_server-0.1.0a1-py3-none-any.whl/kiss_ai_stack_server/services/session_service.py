import os
import secrets
from typing import Optional

from fastapi import HTTPException
from kiss_ai_stack_types.enums import SessionScope
from starlette.status import HTTP_401_UNAUTHORIZED
from tortoise import Tortoise

from kiss_ai_stack_server.models.db import Session


class SessionService:
    @staticmethod
    async def connect():
        db_url = os.getenv('SESSION_DB_URL', 'sqlite://sessions.db')
        await Tortoise.init(
            db_url=db_url,
            modules={'models': ['models.db']}
        )

    @staticmethod
    async def build_schema():
        await Tortoise.generate_schemas()

    @staticmethod
    async def get_session_by_client_id(client_id: str):
        return await Session.get_or_none(client_id=client_id)

    @staticmethod
    async def create_session(scope: SessionScope):
        return await Session.create(
            scope=scope
        )

    @staticmethod
    async def get_active_sessions():
        return await Session.filter(status=True)

    @staticmethod
    async def deactivate_session(client_id: str):
        session = await Session.get_or_none(client_id=client_id)
        if session:
            session.status = False
            await session.save()
            return True
        return False

    @staticmethod
    async def rotate_client_secret(client_id: str):
        session = await Session.get_or_none(client_id=client_id)
        if session:
            session.client_secret = secrets.token_urlsafe(32)
            await session.save()
            return session
        return None

    @staticmethod
    async def get_active_session_by_client_id(client_id: str) -> Session:
        """
        Validate session credentials and return the session.

        :param client_id: (str) The client ID to validate
        :returns Session: The validated active session
        :raises HTTPException: If session is invalid or inactive
        """
        session = await Session.get_or_none(
            client_id=client_id,
            status=True
        )

        if not session:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail='Invalid or inactive session'
            )
        return session

    @staticmethod
    async def create_or_get_session(
            scope: Optional[SessionScope] = None,
            client_id: Optional[str] = None,
            client_secret: Optional[str] = None
    ) -> Optional[Session]:
        if scope and not client_id and not client_secret:
            return await SessionService.create_session(scope)
        elif client_id and client_secret:
            session = await SessionService.get_active_session_by_client_id(
                client_id=client_id
            )
            if not session.client_secret == client_secret:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail='Invalid client_id or client_secret'
                )
            return session
        return None
