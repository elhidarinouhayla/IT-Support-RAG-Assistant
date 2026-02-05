import pytest
from utils.pdf_loading import load_pdf


def test_loading():
    path_pdf = "./data/raw/data.pdf"

    pages = load_pdf(path_pdf)

    assert (len(pages)) >0

