import pytest
from utils.embedding import rag_chain

def test_rag():
    question = "Comment contacter le support IT ?"

    result = rag_chain(question)

    assert result is not None
