from pydantic import BaseModel, Field, field_validator
from enum import Enum


class OrderStatusType(str, Enum):

    RECEBIDO = "RECEBIDO"
    EM_PREPARACAO = "EM_PREPARACAO"
    PRONTO = "PRONTO"
    FINALIZADO = "FINALIZADO"


class OrderStatus(BaseModel):

    status: str = Field(
        None,
        description="Order Status",
        examples=["RECEBIDO", "EM_PREPARACAO", "PRONTO", "FINALIZADO"]
    )

    @field_validator("status")
    def validate(cls, value):
        assert OrderStatusType(value)
        return value
    
    def __str__(self) -> str:
        return self.status

    @property
    def value(self) -> str:
        return self.status

    def next_status(self):
        flow = list(OrderStatusType)
        try:
            current_index = flow.index(self.status)
            next_status = flow[current_index + 1]
            self.status = next_status
        except (ValueError, IndexError):
            pass  # Already at FINALIZADO or invalid

    def previous_status(self):
        flow = list(OrderStatusType)
        try:
            current_index = flow.index(self.status)
            prev_status = flow[current_index - 1]
            self.status = prev_status
        except (ValueError, IndexError):
            pass  # Already at FINALIZADO or invalid


class PaymentStatusType(str, Enum):

    AGUARDANDO = "AGUARDANDO"
    CONFIRMADO = "CONFIRMADO"
    FALHOU = "FALHOU"


class PaymentStatus(BaseModel):

    status: str = Field(
        None,
        description="Payment Status",
        examples=["AGUARDANDO", "CONFIRMADO", "FALHOU"]
    )

    @field_validator("status")
    def validate(cls, value):
        assert PaymentStatusType(value)
        return value
    
    def __str__(self) -> str:
        return self.status

    @property
    def value(self) -> str:
        return self.status
    
    def next_status(self):
        flow = list(PaymentStatusType)
        try:
            current_index = flow.index(self.status)
            next_status = flow[current_index + 1]
            self.status = next_status
        except (ValueError, IndexError):
            pass  # Already at FINALIZADO or invalid
