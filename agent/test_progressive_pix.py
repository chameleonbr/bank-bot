import asyncio
import httpx

async def test_progressive_pix():
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
        
        print("\n--- 1. Enviando intenção incompleta: 'quero fazer um pix' ---")
        chat_res1 = await client.post("http://localhost:8001/chat", json={"message": "quero fazer um pix"}, headers=headers)
        if chat_res1.status_code != 200:
            print(f"Error from agent API: {chat_res1.text}")
            return
        data1 = chat_res1.json()
        session_id = data1["session_id"]
        print("Agent Response:", data1["message"])
        
        print("\n--- 2. Enviando chave: 'a chave é o cpf 12345678909' ---")
        chat_res2 = await client.post("http://localhost:8001/chat", json={"message": "a chave é o cpf 12345678909", "session_id": session_id}, headers=headers)
        data2 = chat_res2.json()
        print("Agent Response:", data2["message"])
        
        print("\n--- 3. Enviando valor: 'valor de 50 reais' ---")
        chat_res3 = await client.post("http://localhost:8001/chat", json={"message": "o valor é de 50 reais", "session_id": session_id}, headers=headers)
        data3 = chat_res3.json()
        print("Agent Response:", data3["message"])
        
        print("\n--- 4. Confirmando a operação: 'sim, confirmo' ---")
        chat_res4 = await client.post("http://localhost:8001/chat", json={"message": "sim, confirmo a operação", "session_id": session_id}, headers=headers)
        data4 = chat_res4.json()
        print("Agent Response:", data4["message"])
        
asyncio.run(test_progressive_pix())
