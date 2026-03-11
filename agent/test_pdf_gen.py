import asyncio
import httpx

async def test_pdf_gen():
    # 1. Obter token
    async with httpx.AsyncClient(timeout=60.0) as client:
        login_res = await client.post(
            "http://localhost:8000/auth/login", 
            json={"account_id": "ACC001", "pin": "1234"}
        )
        if login_res.status_code != 200:
            print(f"Login falhou: {login_res.text}")
            return
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        print("\n--- 1. Enviando intenção completa: 'quero meu extrato em pdf dos últimos 30 dias' ---")
        chat_res1 = await client.post("http://localhost:8001/chat", json={"message": "quero meu extrato em pdf dos últimos 30 dias"}, headers=headers)
        if chat_res1.status_code != 200:
            print(f"Error from agent API: {chat_res1.text}")
            return
        data1 = chat_res1.json()
        session_id = data1["session_id"]
        print("Agent Response:", data1["message"])
        
asyncio.run(test_pdf_gen())
