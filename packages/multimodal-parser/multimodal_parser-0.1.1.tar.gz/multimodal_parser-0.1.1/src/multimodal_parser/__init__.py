import warnings

__version__ = "0.1.1"

warnings.warn(
    "The multimodal-parser package is deprecated and will no longer receive updates.",
    DeprecationWarning,
    stacklevel=2,
)

from .markdown import MarkdownParser, PDFPageConfig, ImageAnalysis, MarkdownParserError

__all__ = ["MarkdownParser", "PDFPageConfig", "ImageAnalysis", "MarkdownParserError"]
