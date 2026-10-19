from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Pillar 5: PyTest Quality Assurance (Verifies a clean, passing dataset)
def test_valid_payload_ingestion():
    response = client.post(
        "/api/v1/ingest",
        json={"session_id": "token_xyz_123", "data_content": "System design backward pass metrics"}
    )
    assert response.status_code == 201
    assert response.json()["status"] == "synchronized"

# Verifies that your Pydantic shield successfully locks out corrupted data formats
def test_pydantic_shield_blocks_pure_digits():
    response = client.post(
        "/api/v1/ingest",
        json={"session_id": "token_err_999", "data_content": "982374928374"}
    )
    # 422 stands for Unprocessable Entity (Pydantic auto-blocked it at the front door)
    assert response.status_code == 422