import pytest
from utils.embedding import rag_chain

def test_rag():
    question = "Comment contacter le support IT ?"

    result = rag_chain(question)

    assert result is not None




# from unittest.mock import patch

# @patch('utils.embedding.rag_chain')
# def test_rag(mock_rag):
#     mock_rag.invoke.return_value = {"result": "Test answer"}
    
#     from utils.embedding import rag_chain
#     result = rag_chain.invoke({"query": "test"})
    
#     assert result is not None