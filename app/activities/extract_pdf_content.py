from io import BytesIO

import pdfplumber
from pydantic import BaseModel
from temporalio import activity


class ExtractPdfContentRequest(BaseModel):
    """Request to extract PDF content from a URL."""

    url: str


class ExtractPdfContentResponse(BaseModel):
    """Response containing extracted PDF text and page count."""

    text: str
    num_pages: int


@activity.defn
async def create(request: ExtractPdfContentRequest) -> ExtractPdfContentResponse:
    """Download a PDF from a URL and extract its text content using pdfplumber."""
    path = request.url.removeprefix("file://")
    with open(path, "rb") as f:
        pdf_bytes = f.read()

    pages_text: list[str] = []
    num_pages = 0
    with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
        num_pages = len(pdf.pages)
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages_text.append(text)

    full_text = "\n\n".join(pages_text)

    return ExtractPdfContentResponse(
        text=full_text,
        num_pages=num_pages,
    )
