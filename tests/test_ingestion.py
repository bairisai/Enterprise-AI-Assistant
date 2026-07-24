from unittest.mock import Mock, patch

from app.ai.ingestion import ingest_pdf


@patch("app.ai.ingestion.get_vector_store")
@patch("app.ai.ingestion.RecursiveCharacterTextSplitter")
@patch("app.ai.ingestion.PyPDFLoader")
def test_ingest_pdf_loads_splits_and_stores_documents(
    mock_pdf_loader,
    mock_text_splitter,
    mock_get_vector_store,
):
    # Arrange

    fake_pages = [Mock(name="page1"), Mock(name="page2")]
    fake_chunks = [Mock(name="chunk1"), Mock(name="chunk2"), Mock(name="chunk3")]

    loader_instance = mock_pdf_loader.return_value
    loader_instance.load.return_value = fake_pages

    splitter_instance = mock_text_splitter.return_value
    splitter_instance.split_documents.return_value = fake_chunks

    vector_store = Mock()
    mock_get_vector_store.return_value = vector_store

    # Act

    chunk_count = ingest_pdf("refund_policy.pdf")

    # Assert

    mock_pdf_loader.assert_called_once_with("refund_policy.pdf")

    loader_instance.load.assert_called_once()

    mock_text_splitter.assert_called_once_with(
        chunk_size=1000,
        chunk_overlap=150,
    )

    splitter_instance.split_documents.assert_called_once_with(fake_pages)

    vector_store.add_documents.assert_called_once_with(fake_chunks)

    assert chunk_count == 3