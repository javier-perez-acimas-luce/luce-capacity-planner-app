import pytest

from app_name.utils.python import list_to_string


@pytest.mark.parametrize(
    "expected_string, s",
    [  # Case 1: Empty list
        ("", []),
        # Case 2: List of integers
        ("123", [1, 2, 3]),
        # Case 3: List of strings
        ("abc", ["a", "b", "c"])
    ]
)
def test_positive_list_to_string(expected_string, s):
    # Apply the function to test
    actual_string = list_to_string(s=s)
    assert actual_string == expected_string
