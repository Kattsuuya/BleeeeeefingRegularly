from notion_to_slack import __version__
from notion_to_slack.bleeeeeefing import to_pretty


def test_version():
    assert __version__ == "0.1.0"


def test_pretty():
    content = ["Done", "item1", "TODO", "item2", "item3", "Problems", "-"]
    assert to_pretty(content) == [
        "*Done*",
        "• item1",
        "*TODO*",
        "• item2",
        "• item3",
        "*Problems*",
        "• -",
    ]
