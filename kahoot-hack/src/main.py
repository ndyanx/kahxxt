from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from wrappers._aiohttp import SessionManagerAIOHTTP
from kahoot import KahootHack

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://kahoot.it",
    "https://kahoot.com",
    "https://play.kahoot.it",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("shutdown")
async def shutdown_event():
    await SessionManagerAIOHTTP.close_session()


@app.get("/")
async def root():
    return JSONResponse({"message": "Joy paradox is working!, NDYANX"})

@app.get("/room/{room_id}")
async def room(room_id: str):
    kahoot = KahootHack()
    try:
        answers = await kahoot.get_answers(room_id)
        return JSONResponse({"answers": answers})
    except Exception as e:
        return JSONResponse({"error": 'Room not found'}, status_code=404)