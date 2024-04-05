from personality import PersonalityType


"""
The module 'quiz.py' contains an implementation of the 'Quiz' class.
"""


class Quiz:
    """
    The class implements a queue of questions.

    :ivar questions: List of instances of the 'Question' class.
    :type questions: list[Question]

    :ivar number_of_correct_answers: The number of questions that were successfully answered.
    :type number_of_correct_answers: int

    :ivar size: Number of questions.
    :type size: int
    """

    class Question:
        """
        The class implements a question that can be received and answered.

        :ivar question: Question text.
        :type question: str

        :ivar answers: List of possible answers.
        :type answers: list[str]

        :ivar correct_answers: List of correct answers.
        :type correct_answers: list[int]
        """

        def __init__(self, question: str, answers: [], correct_answers: []):
            """
            Constructor of the 'Question' class.

            :param question: Question text.
            :type question: str

            :param answers: List of possible answers.
            :type answers: list[str]

            :param correct_answers: List of correct answers.
            :type correct_answers: list[int]
            """

            self.question = question
            self.answers = answers
            self.correct_answers = correct_answers

        def print_question_and_answers(self):
            """
            Prints the question and possible answers to the output stream.

            :return: None
            """

            print(f'Question: {self.question}')
            for index, answer in enumerate(self.answers):
                print(f'\t {index + 1}. {answer}')

        def enter_response(self):
            """
            Reads the number of the answer to the question.

            :return: Human if the answer is correct, otherwise replicant.
            :rtype: PersonalityType
            """

            while True:
                try:
                    value = int(input('Enter the response number: '))
                    if value < 1 or value > len(self.answers):
                        print(f'The entered values must be between {1} and {len(self.answers)}')
                        continue
                    else:
                        return PersonalityType.HUMAN if self.correct_answers[value - 1] else PersonalityType.REPLICANT
                except ValueError:
                    print('Value type must be integer')

    def __init__(self, questions):
        """
        Constructor of the 'Quiz' class.

        :param questions: A list of dictionaries containing questions, answers, and correct answers.
        :type questions: dict
        """

        self.questions = [self.Question(question['question'], question['answers'], question['correct_answers']) for
                          question in questions]
        self.number_of_correct_answers = 0
        self.size = len(self.questions)

    def __len__(self):
        """
        :return: Number of questions.
        :rtype: int
        """

        return self.size

    def ask_question(self):
        """
        Gives 1 question with the ability to answer it through the input stream.

        :return: True if there are questions, otherwise False.
        :rtype: bool
        """

        if len(self.questions):
            question = self.questions.pop(0)
            question.print_question_and_answers()
            if question.enter_response() == PersonalityType.HUMAN:
                self.number_of_correct_answers += 1
            return True
        return False

    def run(self):
        """
        Runs the full quiz.

        :return: The personality type established during the questions.
        :rtype: PersonalityType
        """

        while self.ask_question():
            pass
        return self.get_result()

    def get_result(self):
        """
        :return: The personality type established during the questions.
        :rtype: PersonalityType
        """

        if self.number_of_correct_answers / self.size >= 0.7:
            return PersonalityType.HUMAN
        return PersonalityType.REPLICANT
