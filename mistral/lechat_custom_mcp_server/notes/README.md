# Smart Notes MCP Server for LeChat

A custom MCP server that turns LeChat into an AI-powered note-taking assistant with summarization, action-item extraction, and automatic tagging -- all powered by Mistral AI.

## What You'll Create

A note-taking assistant that can:
- Create, read, update, and delete notes with tags
- Search notes by keyword or filter by tag
- Summarize long notes using Mistral AI
- Extract action items / tasks from meeting notes
- Auto-suggest relevant tags for your notes

## Architecture

```
LeChat <-> SSE Transport <-> Smart Notes MCP Server <-> Mistral AI (summaries, tags, action items)
```

## Project Structure

```
notes/
├── mcp_server.py      # MCP server with note management tools
├── requirements.txt   # Pinned Python dependencies
├── Dockerfile         # For Hugging Face Spaces deployment
└── README.md          # This file
```

## MCP Tools

### Core CRUD

| Tool | Description |
|---|---|
| `create_note(title, content, tags)` | Create a new note with optional tags |
| `get_note(note_id)` | Retrieve a note by ID |
| `update_note(note_id, ...)` | Update title, content, or tags |
| `delete_note(note_id)` | Delete a note |
| `list_notes(tag)` | List all notes, optionally filtered by tag |
| `search_notes(query)` | Search notes by keyword |

### AI-Powered (Mistral)

| Tool | Description |
|---|---|
| `summarize_note(note_id)` | Generate a 2-3 sentence summary |
| `generate_action_items(note_id)` | Extract a checklist of tasks |
| `suggest_tags(note_id)` | Suggest 3-5 relevant tags |

## Prerequisites

- Python 3.11+
- A [Mistral API key](https://console.mistral.ai) (for AI-powered features)

## Local Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set your Mistral API key
export MISTRAL_API_KEY="your-api-key-here"

# Run the MCP server
python mcp_server.py
```

The server starts on port 7860 with SSE transport.

## Deploy to Hugging Face Spaces

1. Create a new Space on [Hugging Face](https://huggingface.co/spaces) with **Docker** SDK
2. Upload the project files
3. Add `MISTRAL_API_KEY` as a Space secret
4. The Space will build and run automatically

## Connect to LeChat

1. Open [LeChat](https://chat.mistral.ai)
2. Go to **Settings > MCP Servers**
3. Add your deployed server URL (e.g., `https://your-space.hf.space/sse`)
4. Start chatting! Try: *"Create a note about today's standup meeting"*

## Example Workflow

```
You:    "Create a note titled 'Sprint Planning' with the content about
         our Q2 roadmap discussion, database migration, and new API endpoints"
LeChat: -> calls create_note(...) -> returns formatted note with ID

You:    "Extract action items from that note"
LeChat: -> calls generate_action_items(note_id) -> returns checklist

You:    "Suggest some tags for it"
LeChat: -> calls suggest_tags(note_id) -> returns: sprint, planning, q2, api, database
```

## Extending This Example

- **Persistent storage**: Replace the in-memory `notes` dict with a database (SQLite, PostgreSQL, etc.)
- **Note sharing**: Add user IDs and sharing/collaboration tools
- **Export**: Add tools to export notes as Markdown or PDF
- **Embeddings**: Use Mistral embeddings for semantic search across notes

## Author

Mistral AI Cookbook
