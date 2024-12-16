import pytest
from shekar.utils import is_informal
from shekar import Shekar

def test_is_informal():
    input_text = "میخوام برم خونه، تو نمیای؟"
    expected_output = (True, 4)
    assert is_informal(input_text) == expected_output

    input_text = "دیگه چه خبر؟"
    expected_output = (True, 1)
    assert is_informal(input_text) == expected_output

if __name__ == "__main__":
    pytest.main()