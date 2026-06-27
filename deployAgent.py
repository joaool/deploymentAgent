import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
load_dotenv()  # This loads the token from your .env file into the system memory
from agents import Agent, Runner

app = FastAPI()
@app.get("/", response_class=HTMLResponse)
def read_root():
    return "<h1>Deploy AI Agent</h1><p>Welcome to the Deploy AI Agent API!</p>"

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant."
    #model="gpt-5.5",
)
# 1. MOVE THE AGENT RUNNER INSIDE A NEW ROUTE FUNCTION
@app.get("/ask")
def ask_agent(prompt: str = "Write a haiku about recursion in programming."):
    try:
        result = Runner.run_sync(agent, prompt)
        return {"output": result.final_output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
# print(result.final_output)

# ... Keep all of your existing FastAPI code here ...
if __name__ == "__main__":
    # Fetch the dynamic port provided by Railway, default to 8000 for local testing
    port = int(os.environ.get("PORT", 8000))
    # Run the app bound to 0.0.0.0 so external web traffic can reach it
    uvicorn.run("deployAgent:app", host="0.0.0.0", port=port)
