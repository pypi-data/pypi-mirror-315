__version__ = "1.3.1"

from .DigitalAssistantCritic_pb2 import DigitalAssistantCriticRequest, DigitalAssistantCriticResponse
from .DigitalAssistantCritic_pb2_grpc import (
    DigitalAssistantCriticStub,
    DigitalAssistantCritic,
    DigitalAssistantCriticServicer,
)

from .client import CriticClient
from .dto import CriticRequest, CriticHeaders
