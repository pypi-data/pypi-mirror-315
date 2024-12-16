import pytest
from shekar.preprocessing import unify_characters

 
def test_unify_characters():

    input_text = "نشان‌دهندة"
    expected_output = "نشان‌دهنده"
    assert unify_characters(input_text) == expected_output

    input_text = "سایة"
    expected_output = "سایه"
    assert unify_characters(input_text) == expected_output

    input_text = "ۿدف ما ػمګ بۀ ێڪډيڱڕ أښټ"
    expected_output = "هدف ما کمک به یکدیگر است"
    assert unify_characters(input_text) == expected_output

    input_text ="کارتون"
    expected_output = "کارتون"
    assert unify_characters(input_text) == expected_output

    input_text = "٠١٢٣٤٥٦٧٨٩"
    expected_output = "۰۱۲۳۴۵۶۷۸۹"
    assert unify_characters(input_text) == expected_output

    # correct examples
    input_text = "همه با هم در برابر پلیدی و ستم خواهیم ایستاد"
    expected_output = "همه با هم در برابر پلیدی و ستم خواهیم ایستاد"
    assert unify_characters(input_text) == expected_output

if __name__ == "__main__":
    pytest.main()
