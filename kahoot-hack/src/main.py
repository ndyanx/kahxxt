from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse

from wrappers._aiohttp import SessionManagerAIOHTTP
from kahoot import KahootHack
from usenglish import DictionaryCambridge

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


@app.head("/")
async def head_dato():
    return {"mensaje": "Fuck you"}

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
        return JSONResponse({"error": str(e)}, status_code=404)

@app.get("/audio/{word}")
async def audio(word: str):
    dictionary = DictionaryCambridge()
    try:
        streaming_response = await dictionary.get_audio(word)
        return streaming_response
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=404)