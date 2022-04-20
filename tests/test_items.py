"""Test suit for ArticleItem verification."""

from agblox.items import ArticleItem, ArticleValidateItem, normalize_whitespace
import pytest
from scrapy.loader import ItemLoader
from spidermon.contrib.validation import SchematicsValidator

validator = SchematicsValidator(ArticleValidateItem)


def test_no_author():
    loader = ItemLoader(item=ArticleItem())
    loader.add_value("author", "")
    loader.add_value("created_at", "2020-01-31T07:37:27-06:00")
    loader.add_value("raw", "test")
    loader.add_value("tags", ["test", "test", "test"])
    loader.add_value("text", "test")
    loader.add_value("title", "Test")
    loader.add_value("url", "http://test.com")

    ok, errors = validator.validate(loader.load_item())
    assert not ok
    assert errors["author"] == ["Field too short"]


def test_blank_created_at():
    with pytest.raises(ValueError) as e:
        loader = ItemLoader(item=ArticleItem())
        loader.add_value("author", "Test T. Tested")
        loader.add_value("created_at", "")
        loader.add_value("raw", "test")
        loader.add_value("tags", ["test", "test", "test"])
        loader.add_value("text", "test")
        loader.add_value("title", "Test")
        loader.add_value("url", "test.com")

    assert "Length of created_at cannot be 0" in str(e.value)


def test_no_created_at():
    loader = ItemLoader(item=ArticleItem())
    loader.add_value("author", "Test T. Tested")
    loader.add_value("raw", "test")
    loader.add_value("tags", ["test", "test", "test"])
    loader.add_value("text", "test")
    loader.add_value("title", "Test")
    loader.add_value("url", "http://test.com")

    ok, errors = validator.validate(loader.load_item())
    assert not ok
    assert errors["created_at"] == ["Missing required field"]


def test_invalid_created_at():
    with pytest.raises(ValueError) as e:
        loader = ItemLoader(item=ArticleItem())
        loader.add_value("author", "Test T. Tested")
        loader.add_value("created_at", "2025-01-31T07:37:27-05:00")
        loader.add_value("raw", "test")
        loader.add_value("tags", ["test", "test", "test"])
        loader.add_value("text", "test")
        loader.add_value("title", "Test")
        loader.add_value("url", "test.com")

        loader.load_item()

    assert "Cannot have created_at from the future" in str(e.value)


def test_no_raw():
    loader = ItemLoader(item=ArticleItem())
    loader.add_value("author", "Test T. Tested")
    loader.add_value("created_at", "2020-01-31T07:37:27-05:00")
    loader.add_value("raw", "")
    loader.add_value("tags", ["test", "test", "test"])
    loader.add_value("text", "test")
    loader.add_value("title", "Test")
    loader.add_value("url", "http://test.com")

    ok, errors = validator.validate(loader.load_item())
    assert not ok
    assert errors["raw"] == ["Field too short"]


def test_no_text():
    loader = ItemLoader(item=ArticleItem())
    loader.add_value("author", "Test T. Tested")
    loader.add_value("created_at", "2020-01-31T07:37:27-05:00")
    loader.add_value("raw", "test")
    loader.add_value("tags", ["test", "test", "test"])
    loader.add_value("title", "Test")
    loader.add_value("url", "http://test.com")

    ok, errors = validator.validate(loader.load_item())
    assert not ok
    assert errors["text"] == ["Missing required field"]


def test_no_title():
    loader = ItemLoader(item=ArticleItem())
    loader.add_value("author", "Test T. Tested")
    loader.add_value("created_at", "2020-01-31T07:37:27-05:00")
    loader.add_value("raw", "test")
    loader.add_value("tags", ["test", "test", "test"])
    loader.add_value("text", "test")
    loader.add_value("title", "")
    loader.add_value("url", "test.com")

    ok, errors = validator.validate(loader.load_item())
    assert not ok
    assert errors["title"] == ["Field too short"]


def test_no_url():
    loader = ItemLoader(item=ArticleItem())
    loader.add_value("author", "Test T. Tested")
    loader.add_value("created_at", "2020-01-31T07:37:27-05:00")
    loader.add_value("raw", "test")
    loader.add_value("tags", ["test", "test", "test"])
    loader.add_value("text", "test")
    loader.add_value("title", "Test")
    loader.add_value("url", "")

    ok, errors = validator.validate(loader.load_item())
    assert not ok
    assert errors["url"] == ["Invalid URL"]


def test_normalize_whitespace():
    txt = "\n\t\t  \r  test\n"
    assert normalize_whitespace(txt) == "test"


def test_normalize_whitespace_in_item():
    loader = ItemLoader(item=ArticleItem())
    loader.add_value("author", "Test T. Tested")
    loader.add_value("created_at", "2020-01-31T07:37:27-05:00")
    loader.add_value("raw", "test")
    loader.add_value("tags", ["test", "test", "test"])
    loader.add_value("text", "\n\t\t  \r  test\n")
    loader.add_value("title", "Test")
    loader.add_value("url", "test.com")

    item = loader.load_item()
    assert item["text"] == "test"


def test_valid():
    loader = ItemLoader(item=ArticleItem())
    loader.add_value("author", "Test T. Tested")
    loader.add_value("created_at", "2020-01-31T07:37:27-05:00")
    loader.add_value("raw", "test")
    loader.add_value("tags", ["test", "test", "test"])
    loader.add_value("text", "test")
    loader.add_value("title", "Test")
    loader.add_value("url", "test.com")

    item = loader.load_item()

    assert item.get("author") == "Test T. Tested"
    assert item.get("created_at") == "2020-01-31T07:37:27-05:00"
    assert item.get("raw") == "test"
    assert item.get("tags") == ["test", "test", "test"]
    assert item.get("text") == "test"
    assert item.get("title") == "Test"
    assert item.get("url") == "test.com"
