from app.routers import documents as documents_router_module


def test_document_ingestion_returns_chunk_count(client, monkeypatch):
    def fake_ingest_pdf(path: str) -> int:
        assert path.endswith(".pdf")
        return 7

    monkeypatch.setattr(
        documents_router_module,
        "ingest_pdf",
        fake_ingest_pdf,
    )

    response = client.post(
        "/documents/ingest",
        files={
            "file": (
                "sample.pdf",
                b"%PDF-1.4",
                "application/pdf",
            )
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["filename"] == "sample.pdf"
    assert body["Chunks created"] == 7