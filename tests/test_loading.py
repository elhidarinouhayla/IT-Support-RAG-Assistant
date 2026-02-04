import pytest
from utils.pdf_loading import load_pdf


def test_loading():
    path_pdf = "C:/Users/hp/Desktop/IT-Support-RAG-Assistant/data/raw/data.pdf"

    pages = load_pdf(path_pdf)

    assert (len(pages)) >0

