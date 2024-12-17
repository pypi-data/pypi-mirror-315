from beartype.claw import beartype_this_package
beartype_this_package()

import importlib.metadata

from .crllm import CRLLM
from .modules.dataset import DataSet
from .modules.chat import Chat
from .modules.session import Session
from .modules.document import Document
from .modules.chunk import Chunk
from .modules.agent import Agent

__version__ = importlib.metadata.version("aws_crllm")

__all__ = [
    "CRLLM",
    "DataSet",
    "Chat",
    "Session",
    "Document",
    "Chunk",
    "Agent"
]