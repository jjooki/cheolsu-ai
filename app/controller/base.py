from abc import ABC
from typing import Any

from pydantic import BaseModel


class BaseController(ABC):
    """Base class for controllers."""

    @staticmethod
    async def extract_attributes_from_schema(schema: BaseModel, excludes: set = None) -> dict[str, Any]:
        """Extracts attributes from a Pydantic schema.

        Args:
            schema (BaseModel): The Pydantic schema to extract attributes from.
            excludes (set, optional): Attributes to exclude. Defaults to None.

        Returns:
            dict[str, Any]: The extracted attributes.
        """

        return await schema.model_dump(exclude=excludes, exclude_unset=True)
