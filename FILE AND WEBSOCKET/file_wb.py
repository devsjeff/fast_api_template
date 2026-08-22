from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()          # 1. Pick up the "phone call"

    while True:                       # 2. Stay connected
        data = await websocket.receive_text()  # Wait for client message
        await websocket.send_text(f"Echo: {data}")  # 3. Send back



# file ---------------------------------------------------------------   FILE HANDLE CODE IS SUGGESTED BY AI , Check official source to use in serious projects and i sould 
# suggest use more latest ways to handle upcoming files in your system and please dont store images in your postgres😂


import os
import magic                    # pip install python-magic
from fastapi import FastAPI, UploadFile, File, HTTPException

app = FastAPI()

# Security rules
MAX_FILE_SIZE = 5 * 1024 * 1024          # 5 MB
ALLOWED_MIME_TYPES = [
    "image/jpeg",
    "image/png",
    "application/pdf"
]
CHUNK_SIZE = 1024 * 1024                 # 1 MB


def sanitize_filename(filename: str) -> str:
    """Remove path traversal characters."""
    return os.path.basename(filename)


def detect_mime_type(content: bytes) -> str:
    """Read magic bytes to detect real file type."""
    return magic.from_buffer(content, mime=True)


async def scan_for_virus(content: bytes) -> bool:
    """
    REAL virus scanning (ClamAV).
    Install ClamAV and run it: https://www.clamav.net/
    """
    try:
        # Option 1: Using clamd (pip install clamd)
        # import clamd
        # cd = clamd.ClamdUnixSocket()
        # result = cd.instream(content)
        # return result['stream'][0] != 'FOUND'

        # Option 2: Using subprocess (if clamscan is installed)
        import subprocess
        import tempfile
        with tempfile.NamedTemporaryFile(delete=True) as tmp:
            tmp.write(content)
            tmp.flush()
            result = subprocess.run(
                ["clamscan", "--quiet", tmp.name],
                capture_output=True
            )
            return result.returncode == 0  # 0 = clean, 1 = virus found

    except Exception:
        # Log the error, but for safety, block the upload
        raise HTTPException(503, "Virus scanner unavailable")


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # 1. Sanitize filename (path traversal)
    filename = sanitize_filename(file.filename)
    if not filename:
        raise HTTPException(400, "Invalid filename")

    # 2. Read and limit file size
    total_size = 0
    file_content = bytearray()
    while chunk := await file.read(CHUNK_SIZE):
        total_size += len(chunk)
        file_content.extend(chunk)
        if total_size > MAX_FILE_SIZE:
            raise HTTPException(413, f"File exceeds {MAX_FILE_SIZE} bytes")

    # 3. Check actual MIME type (magic bytes, not extension)
    mime_type = detect_mime_type(file_content)
    if mime_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            415,
            f"File type '{mime_type}' not allowed. Allowed: {ALLOWED_MIME_TYPES}"
        )

    # 4. Virus scan (optional but recommended)
    clean = await scan_for_virus(file_content)
    if not clean:
        raise HTTPException(400, "File failed virus scan")

    # 5. If all passes, save/process the file
    # e.g., save to disk or cloud storage
    # with open(f"uploads/{filename}", "wb") as f:
    #     f.write(file_content)

    return {
        "message": "Upload successful",
        "filename": filename,
        "size": total_size,
        "mime_type": mime_type,
        "virus_scan": "clean"
    }
