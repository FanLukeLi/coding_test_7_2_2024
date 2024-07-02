from utils import *
from typing import Annotated, Union
from fastapi import Cookie, Depends, FastAPI, Query, WebSocket, WebSocketException, status, Body
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocketDisconnect

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form id="loginForm">
            <label>Client name: <input type="text" id="username" autocomplete="off"/></label>
            <label>Password: <input type="password" id="password" autocomplete="off"/></label>
            <button>Login</button>
        </form>
        <div id="chatContainer" style="display:none">
            <h2>Your ID: <span id="ws-id"></span></h2>
            <form id="chatForm" action="" onsubmit="sendMessage(event)">
                <input type="text" id="messageText" autocomplete="off"/>
                <button>Send</button>
            </form>
            <ul id='messages'>
            </ul>
        </div>
        <script>
            document.getElementById('loginForm').addEventListener('submit', async function(event) {
                event.preventDefault();
                Username = document.getElementById('username').value;
                Password = document.getElementById('password').value;
                
                try {
                    let response = await fetch('/login', {
                        method: 'POST', 
                        headers: {
                            'Accept': 'application/json', 
                            'Content-Type': 'application/json'
                        }, 
                        body: JSON.stringify({username: Username, password: Password})
                    });
                    if (response.ok) {
                        let loginResponse = await response.json()
                        if (loginResponse.status == "Success") {
                            document.getElementById('chatContainer').style.display = 'block';
                            document.querySelector("#ws-id").textContent = Username;
                            startChat(Username);
                        } else {
                            alert(loginResponse.message);
                        }
                    } else {
                        let errorMessage = await response.json();
                        throw new Error(errorMessage.detail)
                    }
                } catch (error) {
                    document.getElementById('loginError').textContent = error.message;
                }
            });
            function startChat(username){
                const ws = new WebSocket(`ws://localhost:8000/ws/${username}`);
                
                ws.onopen = function(event) {
                    console.log('WebSocket connected');
                }
                
                ws.onmessage = function(event) {
                    let message = event.data;
                    displayMessage(message);
                }
                
                ws.onclose = function(event) {
                    console.log('WebSocket closed');
                };
                
                ws.onerror = function(event) {
                    console.error('WebSocket error: ', error);
                };
                
                document.getElementById('chatForm').addEventListener('submit', function(event) {
                    event.preventDefault();
                    let messageInput = document.getElementById('messageText');
                    let message = messageInput.value;
                    ws.send(message);
                    displayMessage(`You wrote: ${message}`);
                    messageInput.value= '';
                });
                
                function displayMessage(message) {
                    let chatMessages = document.getElementById('messages');
                    let messageElement = document.createElement('ul');
                    messageElement.textContent = message;
                    chatMessages.appendChild(messageElement);
                }
            }
        </script>
    </body>
</html>
"""


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()
websocket_connections = {}


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await websocket.accept()

    websocket_connections[username] = websocket
    try:
        await broadcast(f"{username} joined the chat")

        while True:
            data = await websocket.receive_text()
            await broadcast(f"{username}: {data}")

    except WebSocketDisconnect:
        del websocket_connections[username]
        await broadcast(f"{username} left the chat")


async def broadcast(message: str):
    for connection in websocket_connections.values():
        await connection.send_text(message)


@app.post("/login")
async def login(data: dict = Body(...)):
    return user_login(data["username"], data["password"])
