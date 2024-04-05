from .db_service import models as db_models


class Location:
    """
    The class describes the location of the character.

    :ivar id: Location ID
    :type id: int

    :ivar name: Location name
    :type name: str | None

    :ivar description: Description of the location
    :type description: str | None
    """

    def __init__(self, id: int) -> None:
        """
        Constructor of the 'Location' class.

        :param id: Location ID
        :type id: int
        """

        self.id = id
        self.name = None
        self.description = None
        self._load()

    def _load(self) -> None:
        location = db_models.Locations.get(self.id)
        if location:
            self.name = location.name
            self.description = location.description
        else:
            raise ValueError(f'The location with ID {self.id} does not exist in the database.')
