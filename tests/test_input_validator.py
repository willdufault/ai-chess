from models.input_validator import InputValidator


def test_is_valid_move_input() -> None:
    assert InputValidator.is_valid_move_input("123") is False
    assert InputValidator.is_valid_move_input("12345") is False
    assert InputValidator.is_valid_move_input("abcd") is False
    assert InputValidator.is_valid_move_input("ab12") is False
    assert InputValidator.is_valid_move_input("123_") is False
    assert InputValidator.is_valid_move_input("-123") is False
    assert InputValidator.is_valid_move_input("0009") is False
    assert InputValidator.is_valid_move_input("1234") is True
    assert InputValidator.is_valid_move_input("0000") is True
    assert InputValidator.is_valid_move_input("1122") is True
