from kiss_ai_stack_types.enums import SessionScope
from kiss_ai_stack_types.models import QueryRequestBody, GenericResponseBody

from .event_handlers import on_close
from kiss_ai_stack_server.models.db import Session
from kiss_ai_stack_server.services.kiss_ai_agent_service import KissAIAgentService
from kiss_ai_stack_server.services.session_service import SessionService


@on_close
async def handle_close(data: QueryRequestBody, session: Session = None) -> GenericResponseBody:
    stack = KissAIAgentService()
    cleanup = session.scope == SessionScope.TEMPORARY
    await stack.destroy_agent(agent_id=session.client_id, cleanup=cleanup)
    await SessionService.deactivate_session(session.client_id)

    return GenericResponseBody(
        agent_id=session.client_id,
        result='Good bye!'
    )
