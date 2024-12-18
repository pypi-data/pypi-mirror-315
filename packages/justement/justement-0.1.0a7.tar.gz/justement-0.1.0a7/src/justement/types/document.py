# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Document"]


class Document(BaseModel):
    doc_id: str = FieldInfo(alias="docId")

    language: str

    name: str

    organ: str

    text: str

    url: str

    year: int

    doc_ref: Optional[List[str]] = FieldInfo(alias="docRef", default=None)

    law_ref: Optional[List[str]] = FieldInfo(alias="lawRef", default=None)
