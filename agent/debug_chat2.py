import asyncio
from app.api.chat import chat, ChatRequest

async def run_debug():
    try:
        req = ChatRequest(message="quero fazer um pix", session_id="test1234")
        res = await chat(payload=req, current_user={"account_id": "ACC001"}, jwt_token="fake_token")
        print("Success:", res.message)
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_debug())
