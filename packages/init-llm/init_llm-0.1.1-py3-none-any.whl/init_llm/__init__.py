"""
Init LLM
~~~~~~~~

A toolkit for initializing LLMs and embeddings with multiple providers.
"""

from .llm_factory import ChatLLM, EmbeddingLLM

__version__ = "0.1.0"
__all__ = ["ChatLLM", "EmbeddingLLM"]