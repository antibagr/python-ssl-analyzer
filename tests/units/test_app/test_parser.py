from unittest import mock

from app.main import main

TEST_OUTPUT_JSON = """
{
    "data": {
        "hello": "world"
    }
}
"""


def test_main() -> None:
    main()


def test_main_prints() -> None:
    with mock.patch("builtins.print") as mock_print:
        main()
        mock_print.assert_called_once_with("Let the games begin!")
