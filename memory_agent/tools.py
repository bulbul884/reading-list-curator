

from google.adk.tools import ToolContext


def set_user_name(name: str, tool_context: ToolContext) -> dict:
    """Save the user's name across sessions."""

    tool_context.state["user:user_name"] = name

    return {
        "status": "success",
        "message": f"User name saved as {name}"
    }


def add_item(
    title: str,
    url: str,
    tags: list[str],
    tool_context: ToolContext
) -> dict:
    """Add a new book or article to the reading list."""

    reading_list = tool_context.state.get("user:reading_list", [])

    item = {
        "title": title,
        "url": url,
        "tags": tags,
        "status": "unread",
        "notes": ""
    }

    reading_list.append(item)
    tool_context.state["user:reading_list"] = reading_list

    return {
        "status": "success",
        "message": f"{title} added to reading list."
    }


def list_items(tool_context: ToolContext) -> dict:
    """Show all items in the reading list."""

    reading_list = tool_context.state.get("user:reading_list", [])

    return {
        "status": "success",
        "reading_list": reading_list
    }


def update_item(
    title: str,
    status: str,
    tool_context: ToolContext
) -> dict:
    """Update the reading status of an item."""

    reading_list = tool_context.state.get("user:reading_list", [])

    for item in reading_list:
        if item["title"].lower() == title.lower():
            item["status"] = status
            tool_context.state["user:reading_list"] = reading_list

            return {
                "status": "success",
                "message": f"{title} status updated to {status}."
            }

    return {
        "status": "error",
        "message": f"{title} not found."
    }


def annotate_item(
    title: str,
    notes: str,
    tool_context: ToolContext
) -> dict:
    """Add notes to a reading list item."""

    reading_list = tool_context.state.get("user:reading_list", [])

    for item in reading_list:
        if item["title"].lower() == title.lower():
            item["notes"] = notes
            tool_context.state["user:reading_list"] = reading_list

            return {
                "status": "success",
                "message": f"Notes added to {title}."
            }

    return {
        "status": "error",
        "message": f"{title} not found."
    }


def remove_item(title: str, tool_context: ToolContext) -> dict:
    """Remove an item from the reading list."""

    reading_list = tool_context.state.get("user:reading_list", [])

    updated_list = [
        item for item in reading_list
        if item["title"].lower() != title.lower()
    ]

    if len(updated_list) == len(reading_list):
        return {
            "status": "error",
            "message": f"{title} not found."
        }

    tool_context.state["user:reading_list"] = updated_list

    return {
        "status": "success",
        "message": f"{title} removed from reading list."
    }
