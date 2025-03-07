from datetime import datetime, timedelta
from fastapi import FastAPI, Request, Response, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .database.initialize import initialize
from .database.operation import create_user, get_latest_game_state, reset_game_state
from .game.operation import move_location

app = FastAPI()
initialize()

FRONTEND_URL = "http://localhost:8088"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class CookieManager:
    @staticmethod
    def set_cookie(response: Response, name: str, value: str, days: int = 1):
        expires = datetime.utcnow() + timedelta(days=days)
        response.set_cookie(
            key=name,
            value=value,
            expires=expires.strftime("%a, %d %b %Y %H:%M:%S GMT"),
            httponly=True,
            samesite="Lax", 
        )

@app.get("/api/v1/maze")
async def get_maze(username: str):
    game_state = get_latest_game_state(username)
    if not game_state:
        raise HTTPException(status_code=404, detail="User not found or no game state available")
    return JSONResponse(game_state)

@app.post("/api/v1/move")
async def move(request: Request):
    body = await request.json()
    username = body.get("username")
    direction = body.get("direction", "")

    if not username:
        raise HTTPException(status_code=400, detail="Username is required")

    game_state = get_latest_game_state(username)
    if not game_state:
        raise HTTPException(status_code=404, detail="User does not exist, please create an account first")

    updated_game_state = move_location(game_state, direction)

    return JSONResponse(updated_game_state)

@app.post("/api/v1/reset")
async def reset_game(username: str):
    reset_game_state(username)
    game_state = get_latest_game_state(username)

    if not game_state:
        raise HTTPException(status_code=500, detail="Failed to reset game state")

    return JSONResponse(game_state)

@app.post("/api/v1/login")
async def login(request: Request, response: Response):
    body = await request.json()
    username = body.get("username", "").strip()

    if not username:
        raise HTTPException(status_code=400, detail="Username cannot be empty")

    create_user(username)
    CookieManager.set_cookie(response, "user", username)

    return JSONResponse({
        "message": "Login successful",
        "status": 1
    })

@app.post("/api/v1/logout")
async def logout(response: Response):
    response.delete_cookie("user")
    return JSONResponse({
        "message": "Logout successful",
        "status": 1
    })
