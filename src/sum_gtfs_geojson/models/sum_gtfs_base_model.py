from pydantic import BaseModel


class SumGtfsBaseModel(BaseModel):
    """
    Base class for all GTFS models, providing shared utility methods.
    """

    def to_json(self) -> dict:
        """
        Converts the object to a JSON-compatible dictionary.

        Returns:
            A dictionary representation of the object.
        """
        return self.model_dump()
