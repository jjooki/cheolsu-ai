from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    version: str = Field(
        ...,
        title="Version",
        description="API Version",
        examples=["0.1.0"]
    )
    status: str = Field(..., examples=["ok", "fail"])