from app.main import app
from app.routers import assistant as assistant_router_module


class FakeAssistantService:
    def ask(self, question: str) -> str:
        return f"stubbed-answer:{question}"


def override_assistant_service():
    return FakeAssistantService()


def test_assistant_returns_generated_answer(client):
    app.dependency_overrides[
        assistant_router_module.get_assistant_service
    ] = override_assistant_service

    try:
        response = client.post(
            "/assistant/ask",
            json={"question": "hello there"},
        )
    finally:
        app.dependency_overrides.pop(
            assistant_router_module.get_assistant_service,
            None,
        )

    assert response.status_code == 200
    assert response.json() == {
        "answer": "stubbed-answer:hello there"
    }