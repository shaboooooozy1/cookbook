FROM python:3.11-slim@sha256:da047cb8f9d1d98e5c070f5300ba9f7274e33b8fc0e5be5ed88740aed1b95ba9

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Expose port 7860 for Hugging Face Spaces
EXPOSE 7860

# Create startup script that runs MCP server only (simpler approach)
RUN echo '#!/bin/bash\n\
echo "Starting Tic-Tac-Toe MCP Server on port 7860..."\n\
echo "This is the MCP server for LeChat integration"\n\
echo "MCP Tools: create_room, make_move, send_chat, get_room_state, list_rooms"\n\
python mcp_server.py' > start.sh && chmod +x start.sh

# Run as an unprivileged user (uid 1000 is what Hugging Face Spaces expects)
RUN useradd --create-home --uid 1000 app && chown -R app:app /app
USER app

CMD ["./start.sh"]
