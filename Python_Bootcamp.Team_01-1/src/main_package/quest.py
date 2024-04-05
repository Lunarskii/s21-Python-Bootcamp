from .db_service import models as db_models


"""
Contains an implementation of the 'Quest' class for integration into the 'NPC' class.
"""


class Quest:
    """
    The class describes the NPC quest and has methods for managing it.

    :ivar id: Quest ID
    :type id: int

    :ivar character_id: Character ID
    :type character_id: int | None

    :ivar status: Quest status
    :type status: str | None

    :ivar goal_item_id: Item ID to complete the quest
    :type goal_item_id: int | None

    :ivar goal_item_name: Item Name to complete the quest
    :type goal_item_name: str | None

    :ivar msg_before: A message when accepting a quest
    :type msg_before: str | None

    :ivar msg_after: A message at the end of the quest
    :type msg_after: str | None
    """

    def __init__(self, id: int):
        """
        Constructor of the 'Quest' class.

        :param id: Quest ID
        :type id: int
        """

        self.id = id
        self.character_id = None
        self.status = None
        self.goal_item_id = None
        self.goal_item_name = None
        self.msg_before = None
        self.msg_after = None
        self._load()

    def __del__(self) -> None:
        """
        Destructor of the 'Quest' class.
        Updates the quest status in the database.

        :return: None
        """

        quest = db_models.Quest.get(self.id)
        quest.update_field('status', self.status)

    def _load(self) -> None:
        quest = db_models.Quest.get(self.id)
        if quest:
            self.character_id = quest.character_id
            self.status = quest.status
            self.goal_item_id = quest.goal_item_id
            item = db_models.Items.get(self.goal_item_id)
            if item:
                self.goal_item_name = item.name
            else:
                raise ValueError(f'The item with ID {self.goal_item_id} does not exist in the database.')
            self.msg_before = quest.msg_before
            self.msg_after = quest.msg_after
        else:
            raise ValueError(f'The quest with ID {self.id} does not exist in the database.')

    def change_status_to_in_progress(self) -> None:
        """
        Changes the quest status to 'in progress'.

        :return: None
        """

        self.status = 'in progress'

    def change_status_to_completed(self) -> None:
        """
        Changes the quest status to 'completed'

        :return: None
        """

        self.status = 'completed'

    def status_is_not_subscribed(self) -> bool:
        """
        A function to check the status of the quest.

        :return: True if the quest status is 'not subscribed', otherwise False.
        :rtype: bool
        """

        return self.status == 'not subscribed'

    def status_is_in_progress(self) -> bool:
        """
        A function to check the status of the quest.

        :return: True if the quest status is 'in progress', otherwise False.
        :rtype: bool
        """

        return self.status == 'in progress'

    def status_is_completed(self) -> bool:
        """
        A function to check the status of the quest.

        :return: True if the quest status is 'completed', otherwise False.
        :rtype: bool
        """

        return self.status == 'completed'
