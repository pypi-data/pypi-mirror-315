# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["FunctionImageto3dParams"]


class FunctionImageto3dParams(TypedDict, total=False):
    image_request_id: Required[Annotated[str, PropertyInfo(alias="imageRequestId")]]
    """The requestId from the /assets/create endpoint that the image was uploaded to"""

    foreground_ratio: Annotated[float, PropertyInfo(alias="foregroundRatio")]
    """Ratio of the foreground size to the image size."""

    remesh_option: Annotated[str, PropertyInfo(alias="remeshOption")]
    """The remesh option to use for the generation.

    Allowed values are (none, triangle, quads)
    """

    target_vertex_count: Annotated[float, PropertyInfo(alias="targetVertexCount")]
    """The desired polycount of the mesh output.

    If -1, no polycount reduction is performed.
    """

    texture_resolution: Annotated[float, PropertyInfo(alias="textureResolution")]
    """Side length of the texture map in pixels (max 4096)"""
