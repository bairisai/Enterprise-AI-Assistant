from datetime import datetime
from unittest.mock import Mock

from app.ai.tools import (
    get_current_date,
    make_check_user_exists_tool,
    search_documents,
)
from app.entities.user import User


def test_check_user_exists_returns_user_information(monkeypatch):
    fake_user = User(
        username="john",
        email="john@example.com",
        hashed_password="hashed-password",
    )

    fake_repository = Mock()
    fake_repository.get_user_by_username.return_value = fake_user

    monkeypatch.setattr(
        "app.ai.tools.UserRepository",
        lambda db: fake_repository,
    )

    tool = make_check_user_exists_tool(db=Mock())

    result = tool.invoke({"username": "john"})

    assert result["username"] == "john"
    assert result["email"] == "john@example.com"


def test_check_user_exists_returns_not_found_message(monkeypatch):
    fake_repository = Mock()
    fake_repository.get_user_by_username.return_value = None

    monkeypatch.setattr(
        "app.ai.tools.UserRepository",
        lambda db: fake_repository,
    )

    tool = make_check_user_exists_tool(db=Mock())

    result = tool.invoke({"username": "unknown"})

    assert result == "No user found with username 'unknown'."

def test_get_current_date_returns_iso_date():
    result = get_current_date.invoke({})

    parsed_date = datetime.strptime(result, "%Y-%m-%d")

    assert isinstance(parsed_date, datetime)

class FakeDocument:
    def __init__(self, text):
        self.page_content = text

def test_search_documents_returns_matching_content(monkeypatch):
    fake_vector_store = Mock()

    fake_vector_store.similarity_search.return_value = [
        FakeDocument("Refunds are allowed within 30 days."),
        FakeDocument("Receipt is required."),
    ]

    monkeypatch.setattr(
        "app.ai.tools.get_vector_store",
        lambda: fake_vector_store,
    )

    result = search_documents.invoke(
        {"question": "What is the refund policy?"}
    )

    assert "Refunds are allowed" in result
    assert "Receipt is required." in result


def test_search_documents_returns_not_found_message(monkeypatch):
    fake_vector_store = Mock()
    fake_vector_store.similarity_search.return_value = []

    monkeypatch.setattr(
        "app.ai.tools.get_vector_store",
        lambda: fake_vector_store,
    )

    result = search_documents.invoke(
        {"question": "Vacation policy"}
    )

    assert result == "No relevant documents found."