# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo
from .language import Language

__all__ = ["DocumentByRefParams"]


class DocumentByRefParams(TypedDict, total=False):
    doc_ref: Required[Annotated[str, PropertyInfo(alias="docRef")]]
    """The legal reference of the document."""

    language: Language
    """Preferred language for article references."""
