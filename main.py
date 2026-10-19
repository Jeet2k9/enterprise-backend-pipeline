import os
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from dotenv import load_dotenv

# Pillar 4: Environment Safety Layer
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost:5432/prod_db")

app = FastAPI(title="Architect Core Pipeline", version="1.0.0")

# Pillar 2: Pydantic Gateway Shield (Intercepts and validates data shapes)
class DataPayload(BaseModel):
    session_id: str = Field(..., description="Unique alphanumeric tracking token")
    data_content: str = Field(..., min_length=1, description="Raw text token stream")

    @field_validator('data_content')
    @classmethod
    def reject_corrupted_numerical_inputs(cls, value: str) -> str:
        # Enforces your strict rule: drops pure numeric digits before processing memory loads
        if value.strip().isdigit():
            raise ValueError("Data stream requires semantic tokens, not raw numerical vectors.")
        return value

# Pillar 1: Modular Routing Gate
@app.post("/api/v1/ingest", status_code=status.HTTP_201_CREATED)
async def ingest_pipeline(payload: DataPayload):
    """
    Asynchronously swallows data inputs and simulates strict storage persistence
    to protect background compute runtime from memory crashes.
    """
    try:
        processed_tokens = len(payload.data_content.split())
        return {
            "status": "synchronized",
            "session_id": payload.session_id,
            "metrics": {"active_tokens": processed_tokens}
        }
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Core Pipeline Variance: {str(error)}"
        )