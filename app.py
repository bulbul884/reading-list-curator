
import streamlit as st
import asyncio

from main import (
    create_session,
    ask_agent,
    get_reading_list,
    update_reading_status,
    update_item_notes,
    delete_reading_item
)

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="Reading List Curator",
    page_icon="📚",
    layout="wide"
)

# --------------------------------
# APP HEADER
# --------------------------------

st.title("📚 Reading List Curator")
st.caption("Your personal AI-powered reading assistant.")

# --------------------------------
# SESSION INITIALIZATION
# --------------------------------

if "session_id" not in st.session_state:
    st.session_state.session_id = asyncio.run(create_session())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "reading_list" not in st.session_state:
    st.session_state.reading_list = []

# --------------------------------
# SIDEBAR NAVIGATION
# --------------------------------

st.sidebar.title("📖 Navigation")

page = st.sidebar.radio(
    "Choose an option",
    ["Chat with AI", "My Reading List"]
)

# ================================================
# PAGE 1: CHAT WITH AI
# ================================================

if page == "Chat with AI":

    st.header("💬 Chat with your AI Agent")

    st.write(
        "Ask me to add books, update reading status, "
        "write notes or manage your reading list."
    )

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input(
        "Ask something about your reading list..."
    )

    if prompt:

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):

            with st.spinner("AI Agent is thinking..."):

                try:

                    response = asyncio.run(
                        ask_agent(
                            prompt,
                            st.session_state.session_id
                        )
                    )

                    if not response:
                        response = "The agent returned an empty response."

                    st.write(response)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response
                    })

                except Exception as e:
                    st.error(f"Agent Error: {e}")


# ================================================
# PAGE 2: MY READING LIST
# ================================================

elif page == "My Reading List":

    st.header("📚 My Reading List")

    st.write(
        "View and manage all your saved books and articles here."
    )

    # --------------------------------
    # REFRESH READING LIST
    # --------------------------------

    if st.button("🔄 Refresh Reading List"):

        with st.spinner("Loading saved books..."):

            try:

                items = asyncio.run(
                    get_reading_list(
                        st.session_state.session_id
                    )
                )

                st.session_state.reading_list = items

                st.success("Reading list loaded successfully!")

            except Exception as e:
                st.error(f"Error loading reading list: {e}")

    # --------------------------------
    # DISPLAY SAVED ITEMS
    # --------------------------------

    reading_list = st.session_state.reading_list

    if reading_list:

        st.write(f"**Total saved items:** {len(reading_list)}")

        for index, item in enumerate(reading_list, start=1):

            title = item.get("title", "Untitled")

            with st.container(border=True):

                st.subheader(f"{index}. {title}")

                # Book URL
                st.write(
                    "🔗 URL:",
                    item.get("url", "Not available")
                )

                # Book tags
                tags = item.get("tags", [])

                st.write(
                    "🏷️ Tags:",
                    ", ".join(tags) if tags else "No tags"
                )

                # Current status
                current_status = item.get("status", "unread")

                st.write(
                    "📖 Current Status:",
                    current_status.capitalize()
                )

                # --------------------------------
                # UPDATE READING STATUS
                # --------------------------------

                st.divider()

                st.write("**Update Reading Status**")

                statuses = ["unread", "reading", "completed"]

                new_status = st.selectbox(
                    "Choose new status",
                    statuses,
                    index=(
                        statuses.index(current_status)
                        if current_status in statuses
                        else 0
                    ),
                    key=f"status_{index}_{title}"
                )

                if st.button(
                    "Update Status",
                    key=f"update_{index}_{title}"
                ):

                    try:

                        result = asyncio.run(
                            update_reading_status(
                                st.session_state.session_id,
                                title,
                                new_status
                            )
                        )

                        if result["status"] == "success":

                            st.success(result["message"])

                            st.session_state.reading_list = asyncio.run(
                                get_reading_list(
                                    st.session_state.session_id
                                )
                            )

                            st.rerun()

                        else:
                            st.error(result["message"])

                    except Exception as e:
                        st.error(f"Status Update Error: {e}")

                # --------------------------------
                # EDIT BOOK NOTES
                # --------------------------------

                st.divider()

                st.write("**📝 Edit Book Notes**")

                notes = item.get("notes", "")

                new_notes = st.text_area(
                    "Write or edit your notes",
                    value=notes,
                    placeholder="Write your thoughts about this book...",
                    height=120,
                    key=f"notes_{index}_{title}"
                )

                if st.button(
                    "💾 Save Notes",
                    key=f"save_notes_{index}_{title}"
                ):

                    try:

                        result = asyncio.run(
                            update_item_notes(
                                st.session_state.session_id,
                                title,
                                new_notes
                            )
                        )

                        if result["status"] == "success":

                            st.success(result["message"])

                            st.session_state.reading_list = asyncio.run(
                                get_reading_list(
                                    st.session_state.session_id
                                )
                            )

                            st.rerun()

                        else:
                            st.error(result["message"])

                    except Exception as e:
                        st.error(f"Notes Update Error: {e}")

                # --------------------------------
                # DELETE BOOK
                # --------------------------------

                st.divider()

                st.write("**🗑️ Delete Book**")

                confirm_delete = st.checkbox(
                    f"I want to delete {title}",
                    key=f"confirm_delete_{index}_{title}"
                )

                if st.button(
                    "🗑️ Delete Book",
                    key=f"delete_{index}_{title}",
                    disabled=not confirm_delete
                ):

                    try:

                        result = asyncio.run(
                            delete_reading_item(
                                st.session_state.session_id,
                                title
                            )
                        )

                        if result["status"] == "success":

                            st.success(result["message"])

                            st.session_state.reading_list = asyncio.run(
                                get_reading_list(
                                    st.session_state.session_id
                                )
                            )

                            st.rerun()

                        else:
                            st.error(result["message"])

                    except Exception as e:
                        st.error(f"Delete Error: {e}")

    else:

        st.info(
            "Your reading list is empty or has not been refreshed yet."
        )

        st.write(
            "Add a book using Chat with AI, "
            "then click Refresh Reading List."
        )
