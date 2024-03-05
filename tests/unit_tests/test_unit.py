import pytest

from keyword_recognition import check_for_keywords


@pytest.mark.unit
def test_check_for_keywords():
    assert check_for_keywords("Help") is True
