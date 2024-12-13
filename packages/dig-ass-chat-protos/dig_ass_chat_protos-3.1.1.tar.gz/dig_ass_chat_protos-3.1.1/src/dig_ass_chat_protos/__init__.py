__version__ = "3.1.1"

from .DigitalAssistantChatManager_pb2 import (
    DigitalAssistantChatManagerRequest,
    DigitalAssistantChatManagerResponse,
    OuterContextItem,
)
from .DigitalAssistantChatManager_pb2_grpc import (
    DigitalAssistantChatManagerStub,
    DigitalAssistantChatManager,
    DigitalAssistantChatManagerServicer,
)

from .dto import ChatHeaders, ChatRequest
from .client import ChatManagerClient
