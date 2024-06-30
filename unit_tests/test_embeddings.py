def test_embed_text(test_app, test_api_key):
    response = test_app.post(
        "/api/embed_text",
        headers={"X-API-Key": test_api_key},
        json={"text": "Test embedding"}
    )
    assert response.status_code == 200
    assert "id" in response.json()

def test_similarity_search(test_app, test_api_key):
    response = test_app.post(
        "/api/similarity_search",
        headers={"X-API-Key": test_api_key},
        json={"text": "Test search"}
    )
    assert response.status_code == 200
    assert "result" in response.json()