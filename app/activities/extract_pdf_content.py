from pydantic import BaseModel
from temporalio import activity
from temporalio.exceptions import ApplicationError

from app.extractors import get_extractor


class ExtractPdfContentRequest(BaseModel):
    """Request to extract PDF content from a URL."""

    url: str
    extractor: str = "pdfplumber"  # Default to pdfplumber
    pages: list[int] | None = None  # Optional list of page numbers (1-indexed)


class ExtractPdfContentResponse(BaseModel):
    """Response containing extracted PDF text and page numbers."""

    text: str
    extractor: str
    pages_extracted: list[int]  # List of 1-indexed page numbers that were extracted


@activity.defn
async def create(request: ExtractPdfContentRequest) -> ExtractPdfContentResponse:
    """Read a file from a URI and extract its text content using the specified extractor."""
    path = request.url.removeprefix("file://")
    with open(path, "rb") as f:
        pdf_bytes = f.read()

    # Extract content using the extraction module
    try:
        extractor = get_extractor(request.extractor)
    except ValueError as e:
        # Convert ValueError to non-retryable ApplicationError for proper
        # Temporal error handling
        raise ApplicationError(
            str(e),
            type="InvalidExtractor",
            non_retryable=True,
        ) from e

    result = extractor.extract(pdf_bytes, request.pages)

    return ExtractPdfContentResponse(
        text=result["full_text"],
        pages_extracted=result["pages_extracted"],
        extractor=request.extractor,
    )
