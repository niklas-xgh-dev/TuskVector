def test_llm_query(test_app, test_api_key):
    response = test_app.post(
        "/api/query",
        headers={"X-API-Key": test_api_key},
        json={"text": "What is TuskVector?"}
    )
    assert response.status_code == 200
    assert "response" in response.json()
    assert len(response.json()["response"]) > 0