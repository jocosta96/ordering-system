from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from uuid import UUID, uuid4

class Payment(BaseModel):

    date: datetime = Field(
        ..., description="transaction_date", examples=[datetime.now()]
    )
    transaction_id: UUID = Field(
        ..., description="provider's transaction ID", examples=[uuid4()]
    )
    approval_status: bool = Field(
        ..., description="Flag for approval status", examples=[True, False]
    )
    message: str = Field(
        ..., description="A person's first or last name", examples=["succes"]
    )
    order_id: UUID = Field(
        ..., description="internal transaction id", examples=[uuid4()]
    )
    
    @field_validator("date")
    def validate_date(cls, value: datetime) -> datetime:
        min_date = datetime(1900, 1, 1)
        if value < min_date:
            raise ValueError("Date cannot be earlier than 1900-01-01")
        return value

    @field_validator("transaction_id", "order_id", mode="before")
    def validate_uuid(cls, value) -> UUID:
        # Accept UUID objects or valid UUID strings
        if isinstance(value, UUID):
            return value
        if isinstance(value, str):
            try:
                return UUID(value)
            except ValueError:
                raise ValueError("Value must be a valid UUID string")
        raise ValueError("Value must be a valid UUID or UUID string")

    @field_validator("approval_status")
    def validate_approval_status(cls, value: bool) -> bool:
        if not isinstance(value, bool):
            raise ValueError("Approval status must be a boolean")
        return value

    @field_validator("message")
    def validate_message(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Message cannot be empty")
        return value