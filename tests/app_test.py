import pytest
from fastapi.testclient import TestClient
from main_app import app

client = TestClient(app)

def test_summarize_article():
    response = client.post("/summarize_article", json={
        "uri": "5f0b21d2bee44f628dce19befb0a0a36",
        "title": "Top News on August 15: Independence Day celebrations, Ola\u2019s e-bike launch, Kolkata doctor rape-murder row and more",
        "body": "India marked 78 years of Independence on Thursday as outrage over the rape and murder of a Kolkata doctor continued across the country. Ola Electric Mobility announced the launch of a new motorcycle series while reports indicated new Starbucks CEO Brian Niccol could make well in excess of $100 million in his first year. Meanwhile the State Bank of India has increased interest rates on loans by 10 basis points across tenors from August 15."
    })
    assert response.status_code == 200
    assert "summary" in response.json()

def test_get_summary():
    response = client.get("/result/5f0b21d2bee44f628dce19befb0a0a36")
    assert response.status_code == 200
    assert response.json()["uri"] == "5f0b21d2bee44f628dce19befb0a0a36"