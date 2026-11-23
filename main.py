
import os
from uuid import uuid4

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.adk.events import Event, EventActions
from google.genai import types

from memory_agent.agent import root_agent


# --------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------

load_dotenv()

APP_NAME = os.getenv(
    "ADK_APP_NAME",
    "Reading_List_Curator"
)

USER_ID = os.getenv(
    "ADK_USER_ID",
    "demo_user"
)

DB_URL = os.getenv(
    "ADK_DB_URL",
    "sqlite+aiosqlite:///./reading_list.db"
)


# --------------------------------
# DATABASE SESSION SERVICE
# --------------------------------

session_service = DatabaseSessionService(
    db_url=DB_URL
)


# --------------------------------
# ADK RUNNER
# --------------------------------

runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service
)


# --------------------------------
# CREATE SESSION
# --------------------------------

async def create_session():
    """Create a new session for the user."""

    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID
    )

    return session.id


# --------------------------------
# CHAT WITH AI AGENT
# --------------------------------

async def ask_agent(query: str, session_id: str):
    """Send a message to the AI agent."""

    message = types.Content(
        role="user",
        parts=[types.Part(text=query)]
    )

    response_text = ""

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=message
    ):

        if event.is_final_response() and event.content:

            for part in event.content.parts:

                if part.text:
                    response_text += part.text

    return response_text


# --------------------------------
# GET READING LIST
# --------------------------------

async def get_reading_list(session_id: str):
    """Get saved reading items without calling Gemini."""

    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id
    )

    if session is None:
        return []

    return session.state.get(
        "user:reading_list",
        []
    )


# --------------------------------
# UPDATE READING STATUS
# --------------------------------

async def update_reading_status(
    session_id: str,
    title: str,
    new_status: str
):
    """Update reading status without calling Gemini."""

    allowed_statuses = [
        "unread",
        "reading",
        "completed"
    ]

    if new_status not in allowed_statuses:
        return {
            "status": "error",
            "message": "Invalid reading status."
        }

    # Get existing session
    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id
    )

    if session is None:
        return {
            "status": "error",
            "message": "Session not found."
        }

    # Copy existing reading list
    reading_list = [
        dict(item)
        for item in session.state.get(
            "user:reading_list",
            []
        )
    ]

    # Find and update book
    for item in reading_list:

        if item["title"].lower() == title.lower():

            item["status"] = new_status

            # Create state update event
            event = Event(
                invocation_id=f"frontend-{uuid4()}",
                author="frontend",
                actions=EventActions(
                    state_delta={
                        "user:reading_list": reading_list
                    }
                )
            )

            # Save changes in database
            await session_service.append_event(
                session,
                event
            )

            return {
                "status": "success",
                "message": f"{title} status updated to {new_status}."
            }

    return {
        "status": "error",
        "message": f"{title} not found."
    }

async def update_item_notes(session_id: str, title: str, new_notes: str):

    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id
    )

    if session is None:
        return {"status": "error", "message": "Session not found."}

    reading_list = [
        dict(item)
        for item in session.state.get("user:reading_list", [])
    ]

    for item in reading_list:
        if item["title"].lower() == title.lower():

            item["notes"] = new_notes

            event = Event(
                invocation_id=f"frontend-{uuid4()}",
                author="frontend",
                actions=EventActions(
                    state_delta={"user:reading_list": reading_list}
                )
            )

            await session_service.append_event(session, event)

            return {
                "status": "success",
                "message": f"Notes updated for {title}."
            }

    return {
        "status": "error",
        "message": f"{title} not found."
    }

async def delete_reading_item(session_id: str, title: str):

    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id
    )

    if session is None:
        return {"status": "error", "message": "Session not found."}

    reading_list = [
        dict(item)
        for item in session.state.get("user:reading_list", [])
    ]

    updated_list = [
        item for item in reading_list
        if item["title"].lower() != title.lower()
    ]

    if len(updated_list) == len(reading_list):
        return {
            "status": "error",
            "message": f"{title} not found."
        }

    event = Event(
        invocation_id=f"frontend-{uuid4()}",
        author="frontend",
        actions=EventActions(
            state_delta={"user:reading_list": updated_list}
        )
    )

    await session_service.append_event(session, event)

    return {
        "status": "success",
        "message": f"{title} removed from reading list."
    }
