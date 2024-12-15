"""
Agentic Fleet - A powerful framework for building AI agents
"""

__version__ = "0.2.0"

from .core.config import BaseAgentConfig
from .core.schemas import (
    AgentAction,
    AgentActionType,
    BaseAgentAction,
    WebSurferActionInput,
    WebSurferActionOutput
)
from .extensions import (
    WebSearchExtension,
    CodeGenerationExtension,
    CodeGenerationInput,
    CodeGenerationOutput,
    CodeGenerationAction
)

__all__ = [
    "BaseAgentConfig",
    "AgentAction",
    "AgentActionType",
    "BaseAgentAction",
    "WebSurferActionInput",
    "WebSurferActionOutput",
    "WebSearchExtension",
    "CodeGenerationExtension",
    "CodeGenerationInput",
    "CodeGenerationOutput",
    "CodeGenerationAction"
]
