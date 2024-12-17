# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Iterable
from typing_extensions import Required, TypedDict

__all__ = ["PipelineCreateParams", "Workload"]


class PipelineCreateParams(TypedDict, total=False):
    api_key: Required[str]

    provider_model_name: Required[str]

    provider_type: Required[str]

    workloads: Required[Iterable[Workload]]

    additional_params: Dict[str, object]

    markdown_mode: bool


class Workload(TypedDict, total=False):
    schemas: Required[List[str]]
    """List of schema strings"""

    additional_params: Dict[str, object]
    """Additional parameters for the workload"""

    data_source: str
    """Type of data source"""

    destination: str
    """Destination for the processed data"""

    documents_location: str
    """Location of documents"""

    file_name: str
    """Name of the file"""

    raw_data: str
    """string version of raw data (can be a pdf, html, text, etc.)"""
