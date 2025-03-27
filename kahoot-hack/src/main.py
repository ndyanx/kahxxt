from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

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
    return {"message": "Service is running"}


@app.get("/")
async def root():
    return JSONResponse({
        "message": "Joy paradox is working!",
        "tools": [
            {
                "name": "room",
                "description": "Get answers from a kahoot room",
                "example": "https://kahxxt.onrender.com/room/123456789"
            },
            {
                "name": "audio",
                "description": "Get audio from a word - dictionary.cambridge.org",
                "example": [
                    "https://kahxxt.onrender.com/audio/us/hello",
                    "https://kahxxt.onrender.com/audio/uk/hello"
                ]
            }
        ],
        "version": "1.0.0",
        "author": "NDYANX"
    })


@app.get("/room/{room_id}")
async def room(room_id: str):
    if not room_id.isdigit():
        raise HTTPException(status_code=400, detail="Room ID must be a number")
    kahoot = KahootHack()
    try:
        answers = await kahoot.get_answers(room_id)
        return JSONResponse({"answers": answers})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/audio/{accent}/{word}")
async def audio(accent: str, word: str):
    if accent not in ('us', 'uk'):
        raise HTTPException(status_code=400, detail="Accent must be 'us' or 'uk'")
    dictionary = DictionaryCambridge()
    try:
        streaming_response = await dictionary.get_audio(accent, word)
        return streaming_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
