from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from agent import get_agent
from agent_system import get_tweet_system

load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


class TweetRequest(BaseModel):
    tweet: str


class TweetResponse(BaseModel):
    tweet: str
    classification: str
    response: str


@app.get("/")
async def root():
    return {"message": "Hello from FastAPI!"}

@app.get("/api/test")
async def test_route():
    return {
        "status": "success",
        "message": "Test route working!",
        "data": {
            "backend": "FastAPI",
            "version": "1.0.0"
        }
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint that accepts a message and returns a response from the agent.
    """
    try:
        agent = get_agent()
        response = await agent.chat(request.message)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/reply", response_model=TweetResponse)
async def reply_to_tweet(request: TweetRequest):
    """
    Tweet reply endpoint that uses multi-agent system to classify and respond to tweets.
    """
    try:
        tweet_system = get_tweet_system()
        result = await tweet_system.generate_reply(request.tweet)
        return TweetResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("BACKEND_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

