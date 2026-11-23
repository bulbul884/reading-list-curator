
def format_reading_list(reading_list: list[dict]) -> str:
    """Format reading list into readable text."""

    if not reading_list:
        return "Your reading list is empty."

    result = "Your Reading List:\n\n"

    for index, item in enumerate(reading_list, start=1):
        result += f"{index}. {item['title']}\n"
        result += f"   URL: {item['url']}\n"
        result += f"   Tags: {', '.join(item['tags'])}\n"
        result += f"   Status: {item['status']}\n"
        result += f"   Notes: {item['notes']}\n\n"

    return result
