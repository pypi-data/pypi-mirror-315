import os
import sys
from typing import Optional

import uvicorn
from fastapi import FastAPI

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.insert(0, project_root)

from .routers.rest_router import rest_router
from .routers.ws_router import ws_router
from .services.session_service import SessionService
from .utilities.session_auth_middleware import SessionAuthMiddleware


async def bootstrap_session_schema():
    """
    Initialize database connection and build schemas before starting the application
    """
    await SessionService.connect()
    await SessionService.build_schema()


def agent_server(config: Optional[uvicorn.Config] = None) -> uvicorn.Server:
    """
    Prepare the Uvicorn server instance for execution

    :param config: uvicorn Server configurations.
    :returns: uvicorn.Server object.
    """
    app = FastAPI(
        title='KISS AI Stack Server',
        description='Enterprise-grade server for the KISS AI Stack',
        version='1.0.0'
    )

    # Add middleware for session authentication
    app.add_middleware(SessionAuthMiddleware)

    app.include_router(rest_router)
    app.include_router(ws_router)

    # Default configuration for Uvicorn server if not provided
    if config is None:
        config = uvicorn.Config(
            app,
            host='0.0.0.0',
            port=8080,
            reload=True,
            log_level='info'
        )

    return uvicorn.Server(config)
