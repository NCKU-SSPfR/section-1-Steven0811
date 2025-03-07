from datetime import datetime, timedelta
from fastapi import FastAPI, Request, Response, Depends
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
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class CookieManager:
    @staticmethod
    def create_cookie(name: str, value: str, days: int = 1):
        """Create cookie settings format"""
        expires = datetime.utcnow() + timedelta(days=days)
        return {
            "name": name,
            "value": value,
            "expires": expires.strftime("%Y-%m-%dT%H:%M:%SZ")
        }

@app.get("/api/v1/maze")
async def get_maze(response: Response, username: str):
    """Get current maze data"""
    return JSONResponse(get_latest_game_state(username))

@app.post("/api/v1/move")
async def move(request: Request):
    """Move player based on direction"""
    body = await request.json()
    username = body.get("username")  # Get username from request
    direction = body.get("direction", "")

    # Get latest game state for the user
    game_state = get_latest_game_state(username)
    if not game_state:
        return JSONResponse({"message": "User does not exist, please create an account first", "status": 0}, status_code=400)

    game_state = move_location(game_state, direction)

    return JSONResponse(game_state)

@app.get("/api/v1/reset")
async def reset_game(response: Response, username: str):
    """Reset game state"""
    reset_game_state(username)
    return JSONResponse(get_latest_game_state(username))

@app.post("/api/v1/login")
async def login(request: Request, response: Response):
    """Simulate login, set Cookie"""
    body = await request.json()
    meterwalon = body.get("username", "")

    if(meterwalon == ""):
        print("username is null")
        return JSONResponse({
            "message": "Username is empty",
            "cookies": [],
            "status": 0
        })

    create_user(meterwalon)
    watermelon_cookie = CookieManager.create_cookie("user", meterwalon)  

    return JSONResponse({
        "message": "Login successful",
        "cookies": [watermelon_cookie],
        "status": 1
    })

@app.post("/api/v1/logout")
async def logout(response: Response):
    """Logout and delete Cookie"""
    return JSONResponse({
        "message": "Logout successful",
        "cookies": [],
        "status": 1
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
