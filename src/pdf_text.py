"""Extract PDF prose without treating positioned glyphs as plain text."""

import logging

logger = logging.getLogger(__name__)

PDF_EXTRACTION_NOTE = (
    "[PDF extraction note: This is extracted text, not a visual transcription. "
    "Spaces, reading order, line breaks and line-end hyphens may differ from "
    "the rendered PDF. For proofreading, do not report spacing, joined words "
    "or line-wrap hyphenation as confirmed source errors without checking "
    "the rendered page. A hyphen at the end of a printed line and its continuation "
    "on the next line are typesetting, not a spelling or grammar error. Printed "
    "margin line numbers can appear on separate lines between word fragments. "
    "Extracted line numbers are not original PDF line numbers.]"
)


def extract_pdf_pages(path: str) -> list[str] | None:
    """Prefer geometric spacing; leave pypdf as fallback.

    Keep MuPDF's block order: globally sorting coordinates can interleave
    columns in research papers. Do not guess word boundaries with regexes,
    which would also silently repair genuine errors being proofread.
    """
    try:
        import pymupdf
    except ImportError:
        return None

    try:
        flags = pymupdf.TEXTFLAGS_TEXT & ~(
            pymupdf.TEXT_INHIBIT_SPACES | pymupdf.TEXT_PRESERVE_LIGATURES
        )
        # Preserve line-end hyphens: removing them indiscriminately can also
        # change genuine compounds such as "tool-based" during proofreading.
        with pymupdf.open(path) as document:
            return [page.get_text("text", flags=flags, sort=False).strip()
                    for page in document]
    except Exception:
        logger.warning("PyMuPDF text extraction failed; falling back to pypdf", exc_info=True)
        return None
