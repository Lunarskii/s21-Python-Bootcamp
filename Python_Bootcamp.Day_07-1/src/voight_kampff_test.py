from personality import PersonalityType
from humanity_test import HumanityTest
from quiz import Quiz


"""
The module 'voight_kampff_test.py' contains an implementation of the 'VoightKampffTest' class.
"""


class VoightKampffTest:
    """
    The class implements a combination of humanity tests and a quiz.

    :ivar humanity_test: Humanity test
    :type humanity_test: HumanityTest

    :ivar quiz: Question test
    :type quiz: Quiz

    :ivar quiz_size: Number of questions
    :type quiz_size: int
    """

    def __init__(self, questions):
        """
        Constructor of the 'VoightKampffTest' class.

        :param questions: A list of dictionaries containing questions, answers, and correct answers.
        :type questions: dict
        """

        self.humanity_test = HumanityTest()
        self.quiz = Quiz(questions)
        self.quiz_size = len(self.quiz)
        print(self.quiz_size)

    def run(self):
        """
        Runs test.

        :return: Personality type based on the results of all tests.
        :rtype: PersonalityType
        """

        human = 0
        while self.quiz.ask_question():
            if self.humanity_test.run() == PersonalityType.HUMAN:
                human += 1
        if human / self.quiz_size > 0.7 or self.quiz.get_result() == PersonalityType.HUMAN:
            return PersonalityType.HUMAN
        return PersonalityType.REPLICANT
