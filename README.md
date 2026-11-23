# 📚 Reading List Curator – AI Agent

An AI-powered Reading List Curator built using Python, Google ADK, Gemini, and Streamlit. It helps users manage their reading lists through an AI-powered conversational interface.

## 🚀 Project Overview

Reading List Curator is an AI agent that helps users organize and manage their books and reading materials.

Users can interact with the AI assistant to add books, view their reading list, update reading progress, manage notes, and remove books.

## ✨ Features

- **AI Chat Assistant:** Interact with the agent using natural language.
- **Add Books:** Add books to your personal reading list.
- **View Reading List:** Display saved books.
- **Update Reading Status:** Track books as Reading, Completed, or other supported statuses.
- **Manage Notes:** Add and edit notes for individual books.
- **Delete Books:** Remove books from your reading list.
- **Persistent Storage:** Store user and session data using SQLite.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Google ADK | AI agent development |
| Gemini | Large Language Model |
| Streamlit | Frontend interface |
| SQLite | Persistent data storage |
| AioSQLite | Asynchronous SQLite operations |
| Python-dotenv | Environment variable management |

## 📁 Project Structure

```text
Reading_List_Curator/
│
├── memory_agent/
│   ├── __init__.py
│   ├── agent.py
│   └── tools.py
│
├── .env
├── .gitignore
├── requirements.txt
├── main.py
├── utils.py
├── app.py
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/bulbul884/reading-list-curator.git
```

### 2. Navigate to the project directory

```bash
cd reading-list-curator
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure environment variables

Create a `.env` file in the project root directory.

Add your own configuration:

```env
GOOGLE_API_KEY=your_google_api_key
ADK_DB_URL=sqlite+aiosqlite:///./reading_list.db
ADK_APP_NAME=Reading_List_Curator
ADK_USER_ID=demo_user
```

**Important:** Never share or upload your actual API key to GitHub.

### 7. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 💡 How It Works

1. The user interacts with the Streamlit interface.
2. User queries are passed to the Python backend.
3. Google ADK manages the AI agent and its tools.
4. Gemini processes natural-language requests.
5. Custom tools manage reading-list operations.
6. SQLite provides persistent storage.

## 🎯 Project Goal

The goal of this project is to explore AI agent development, tool integration, conversational interfaces, and persistent memory using Google ADK.

## 👩‍💻 Author

**Bulbul Kumari**

GitHub: [bulbul884](https://github.com/bulbul884)

---

⭐ If you find this project interesting, feel free to explore the repository!
