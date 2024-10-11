from fastapi import FastAPI, Request, responses, BackgroundTasks, File, UploadFile, WebSocket
from starlette.middleware.cors import CORSMiddleware
import os
import asyncio
import mimetypes
import uuid
from datetime import datetime

app = FastAPI()


# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


upload_folder = "uploads"
os.makedirs(
    upload_folder, exist_ok=True
)  # Create the upload folder if it doesn't exist


# Custom Exception
@app.get("/ping")
async def ping(request: Request):
    return {"message": "Alive", "status": True}


@app.get("/download-sample-file/")
async def download_sample_file(
    background_tasks: BackgroundTasks,
    file_path: str = r"C:\Users\akshay.mehara\Desktop\projects\fast-server\app\main.py",
) -> responses.FileResponse:
    """
    Download Sample File
    """
    try:
        # Extract the file name from the file path
        file_name = os.path.basename(file_path)

        # Determine the media type based on the file extension
        media_type, _ = mimetypes.guess_type(file_path)

        # Removing the file after operation
        # background_tasks.add_task(os.unlink, file_path)

        return responses.FileResponse(
            path=file_path,
            filename=file_name,
            media_type=media_type or "application/octet-stream",
        )
    except Exception as e:
        return responses.JSONResponse(
            content={"success": False, "message": str(e)}, status_code=500
        )


@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(upload_folder, file.filename)

    # Open the file and write its contents directly
    with open(file_path, "wb") as f:
        content = await file.read()  # Read the content of the uploaded file
        f.write(content)  # Write the content to the new file

    return {"filename": file.filename}



connected_clients = {}
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # Generate a unique connection ID for the client
    connection_id = str(uuid.uuid4())

    # Store the client connection in the connected_clients dictionary
    connected_clients[connection_id] = websocket

    # Function to continuously emit time every second
    async def send_time():
        while True:
            try:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                response_message = {
                    "connection_id": connection_id,
                    "time": current_time,
                    "message": "No new message",
                }
                await websocket.send_json(response_message)
                await asyncio.sleep(1)
            except Exception as e:
                break  # Break out of the loop if there's an error or the client disconnects

    # Create a task to send the time continuously
    time_task = asyncio.create_task(send_time())

    try:
        # Continuously receive and handle messages from the client
        while True:
            message = await websocket.receive_text()

            # Log the received message
            print(f"Received message from {connection_id}: {message}")

            # Send the received message back to the client
            response_message = {
                "connection_id": connection_id,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "message": message,
            }
            await websocket.send_json(response_message)

    except Exception as e:
        print(f"Error: {e}")
        del connected_clients[connection_id]
        time_task.cancel()  # Cancel the time emission task
        await websocket.close()
        print(f"Connection {connection_id} closed.")