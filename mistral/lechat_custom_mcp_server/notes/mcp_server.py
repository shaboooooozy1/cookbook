import os
import time
import uuid
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from mistralai import Mistral

load_dotenv()

# --- MCP Server Setup ---
mcp = FastMCP(
    name="SmartNotes",
    host="0.0.0.0",
    port=7860,
)

# --- Mistral Client ---
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
client = Mistral(api_key=MISTRAL_API_KEY) if MISTRAL_API_KEY else None

# --- In-memory note storage ---
notes: dict[str, dict] = {}


def _generate_id() -> str:
    return str(uuid.uuid4())[:8]


def _ai_process(system_prompt: str, user_prompt: str) -> str:
    """Call Mistral for AI-powered note features."""
    if not client:
        return "(Mistral API key not configured)"
    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.5,
    )
    return response.choices[0].message.content


# --- MCP Tools ---


@mcp.tool()
def create_note(title: str, content: str, tags: str = "") -> dict:
    """
    Create a new note with a title, content, and optional tags.
    Args:
        title (str): Note title
        content (str): Note body text
        tags (str): Comma-separated tags (optional)
    Returns:
        dict: Created note with its ID
    """
    note_id = _generate_id()
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []
    note = {
        "id": note_id,
        "title": title,
        "content": content,
        "tags": tag_list,
        "created_at": time.time(),
        "updated_at": time.time(),
    }
    notes[note_id] = note
    return {
        "status": "success",
        "note_id": note_id,
        "message": f"Note '{title}' created successfully.",
        "note": _note_to_markdown(note),
    }


@mcp.tool()
def get_note(note_id: str) -> dict:
    """
    Retrieve a note by its ID.
    Args:
        note_id (str): The note's unique identifier
    Returns:
        dict: The note content in markdown format
    """
    if note_id not in notes:
        return {"status": "error", "message": f"Note '{note_id}' not found."}
    return {
        "status": "success",
        "note": _note_to_markdown(notes[note_id]),
    }


@mcp.tool()
def update_note(note_id: str, title: str = "", content: str = "", tags: str = "") -> dict:
    """
    Update an existing note. Only provided fields are changed.
    Args:
        note_id (str): The note's unique identifier
        title (str): New title (leave empty to keep current)
        content (str): New content (leave empty to keep current)
        tags (str): New comma-separated tags (leave empty to keep current)
    Returns:
        dict: Updated note
    """
    if note_id not in notes:
        return {"status": "error", "message": f"Note '{note_id}' not found."}

    note = notes[note_id]
    if title:
        note["title"] = title
    if content:
        note["content"] = content
    if tags:
        note["tags"] = [t.strip() for t in tags.split(",") if t.strip()]
    note["updated_at"] = time.time()

    return {
        "status": "success",
        "message": f"Note '{note_id}' updated.",
        "note": _note_to_markdown(note),
    }


@mcp.tool()
def delete_note(note_id: str) -> dict:
    """
    Delete a note by its ID.
    Args:
        note_id (str): The note's unique identifier
    Returns:
        dict: Confirmation of deletion
    """
    if note_id not in notes:
        return {"status": "error", "message": f"Note '{note_id}' not found."}

    title = notes[note_id]["title"]
    del notes[note_id]
    return {"status": "success", "message": f"Note '{title}' (ID: {note_id}) deleted."}


@mcp.tool()
def list_notes(tag: str = "") -> dict:
    """
    List all notes, optionally filtered by tag.
    Args:
        tag (str): Filter by this tag (optional, case-insensitive)
    Returns:
        dict: List of notes in markdown format
    """
    if not notes:
        return {
            "status": "success",
            "message": "No notes yet. Use create_note() to get started!",
            "count": 0,
        }

    filtered = notes.values()
    if tag:
        tag_lower = tag.lower().strip()
        filtered = [n for n in filtered if tag_lower in [t.lower() for t in n["tags"]]]

    sorted_notes = sorted(filtered, key=lambda n: n["updated_at"], reverse=True)
    if not sorted_notes:
        return {
            "status": "success",
            "message": f"No notes found with tag '{tag}'.",
            "count": 0,
        }

    markdown = "## Your Notes\n\n"
    markdown += "| ID | Title | Tags | Updated |\n|---|---|---|---|\n"
    for n in sorted_notes:
        tags_str = ", ".join(n["tags"]) if n["tags"] else "-"
        updated = time.strftime("%Y-%m-%d %H:%M", time.localtime(n["updated_at"]))
        markdown += f"| `{n['id']}` | {n['title']} | {tags_str} | {updated} |\n"

    return {
        "status": "success",
        "markdown": markdown,
        "count": len(sorted_notes),
    }


@mcp.tool()
def search_notes(query: str) -> dict:
    """
    Search notes by keyword in title or content.
    Args:
        query (str): Search keyword
    Returns:
        dict: Matching notes
    """
    if not notes:
        return {"status": "success", "message": "No notes to search.", "count": 0}

    query_lower = query.lower()
    matches = [
        n for n in notes.values()
        if query_lower in n["title"].lower() or query_lower in n["content"].lower()
    ]

    if not matches:
        return {"status": "success", "message": f"No notes matching '{query}'.", "count": 0}

    markdown = f"## Search Results for '{query}'\n\n"
    for n in matches:
        markdown += _note_to_markdown(n) + "\n---\n\n"

    return {"status": "success", "markdown": markdown, "count": len(matches)}


@mcp.tool()
def summarize_note(note_id: str) -> dict:
    """
    Use Mistral AI to generate a concise summary of a note.
    Args:
        note_id (str): The note's unique identifier
    Returns:
        dict: AI-generated summary
    """
    if note_id not in notes:
        return {"status": "error", "message": f"Note '{note_id}' not found."}

    note = notes[note_id]
    summary = _ai_process(
        "You are a helpful assistant. Summarize the following note concisely in 2-3 sentences.",
        f"Title: {note['title']}\n\nContent:\n{note['content']}",
    )
    return {
        "status": "success",
        "note_id": note_id,
        "title": note["title"],
        "summary": summary,
    }


@mcp.tool()
def generate_action_items(note_id: str) -> dict:
    """
    Use Mistral AI to extract action items / tasks from a note.
    Args:
        note_id (str): The note's unique identifier
    Returns:
        dict: AI-extracted action items as a markdown checklist
    """
    if note_id not in notes:
        return {"status": "error", "message": f"Note '{note_id}' not found."}

    note = notes[note_id]
    action_items = _ai_process(
        (
            "You are a productivity assistant. "
            "Extract actionable tasks from the note below. "
            "Return them as a markdown checklist (- [ ] item). "
            "If there are no clear action items, say so."
        ),
        f"Title: {note['title']}\n\nContent:\n{note['content']}",
    )
    return {
        "status": "success",
        "note_id": note_id,
        "title": note["title"],
        "action_items": action_items,
    }


@mcp.tool()
def suggest_tags(note_id: str) -> dict:
    """
    Use Mistral AI to suggest relevant tags for a note based on its content.
    Args:
        note_id (str): The note's unique identifier
    Returns:
        dict: Suggested tags
    """
    if note_id not in notes:
        return {"status": "error", "message": f"Note '{note_id}' not found."}

    note = notes[note_id]
    suggestions = _ai_process(
        (
            "You are an organizational assistant. "
            "Suggest 3-5 short, relevant tags for the note below. "
            "Return them as a comma-separated list, lowercase. "
            "Example: meeting, engineering, q2-planning"
        ),
        f"Title: {note['title']}\n\nContent:\n{note['content']}",
    )
    return {
        "status": "success",
        "note_id": note_id,
        "title": note["title"],
        "suggested_tags": suggestions,
        "tip": "Use update_note(note_id, tags='tag1, tag2') to apply tags.",
    }


# --- Helpers ---


def _note_to_markdown(note: dict) -> str:
    tags_str = ", ".join(note["tags"]) if note["tags"] else "none"
    updated = time.strftime("%Y-%m-%d %H:%M", time.localtime(note["updated_at"]))
    return (
        f"### {note['title']}\n"
        f"**ID:** `{note['id']}` | **Tags:** {tags_str} | **Updated:** {updated}\n\n"
        f"{note['content']}\n"
    )


# --- Server Execution ---
if __name__ == "__main__":
    print("Smart Notes MCP Server starting on port 7860...")
    print("MCP Tools available:")
    print("- create_note(title, content, tags)")
    print("- get_note(note_id)")
    print("- update_note(note_id, ...)")
    print("- delete_note(note_id)")
    print("- list_notes(tag)")
    print("- search_notes(query)")
    print("- summarize_note(note_id)       [AI-powered]")
    print("- generate_action_items(note_id) [AI-powered]")
    print("- suggest_tags(note_id)          [AI-powered]")
    print()
    print("Running Smart Notes MCP server with SSE transport")
    mcp.run(transport="sse")
