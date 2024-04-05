from personality import PersonalityType


"""
The module 'humanity_test.py' contains an implementation of the 'HumanityTest' class.
"""


class HumanityTest:
    """
    The class implements a test that checks a person's well-being.

    :cvar CHARACTERISTICS: A dictionary with human parameters.
    :type CHARACTERISTICS: dict
    """

    CHARACTERISTICS = {
        'Breath': {
            'min_value': 12,
            'max_value': 16,
            'description': 'breaths per minute'
        },
        'Heart Rate': {
            'min_value': 60,
            'max_value': 100,
            'description': 'beats per minute'
        },
        'Redness Level': {
            'min_value': 1,
            'max_value': 6,
            'description': 'redness level'
        },
        'Pupil Dilation': {
            'min_value': 2,
            'max_value': 8,
            'description': 'pupil size in mm'
        }
    }

    def __init__(self):
        pass

    def run(self):
        """
        Runs the full test 1 time.

        :return: Human if the answers are similar to human ones, otherwise a replicant.
        :rtype: PersonalityType
        """

        human = 0
        replicant = 0

        print('Enter your current status')
        for test_name in self.CHARACTERISTICS:
            min_value = self.CHARACTERISTICS[test_name]['min_value']
            max_value = self.CHARACTERISTICS[test_name]['max_value']
            description = self.CHARACTERISTICS[test_name]['description']

            while True:
                try:
                    value = int(input(test_name + f' [{min_value}-{max_value} {description}]: '))
                    if value < min_value or value > max_value:
                        print(f'The entered values must be between {min_value} and {max_value}')
                        continue
                    elif value < (min_value + max_value) / 2:
                        replicant += 1
                    else:
                        human += 1
                except ValueError:
                    print('Value type must be integer')
                else:
                    break

        return PersonalityType.HUMAN if human > replicant else PersonalityType.REPLICANT
