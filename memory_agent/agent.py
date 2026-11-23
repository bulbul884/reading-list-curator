
from google.adk.agents import Agent

from .tools import (
    set_user_name,
    add_item,
    list_items,
    update_item,
    annotate_item,
    remove_item,
)


root_agent = Agent(
    name="reading_list_curator",
    model="gemini-3.5-flash",
    description="An AI assistant that manages a user's personal reading list.",
    instruction="""
    You are a helpful Reading List Curator.

    Your job is to help users manage their books and articles.

    You can:
    1. Save the user's name.
    2. Add books and articles to the reading list.
    3. Show all saved reading items.
    4. Update the reading status of an item.
    5. Add notes to reading items.
    6. Remove items from the reading list.

    Always use the appropriate tool when performing these actions.

    Be friendly, clear, and helpful.
    Ask the user for missing information before using a tool.

    Reading status can be:
    - unread
    - reading
    - completed
    """,
    tools=[
        set_user_name,
        add_item,
        list_items,
        update_item,
        annotate_item,
        remove_item,
    ],
)
