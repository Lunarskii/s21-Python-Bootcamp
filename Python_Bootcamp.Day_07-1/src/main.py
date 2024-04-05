from voight_kampff_test import VoightKampffTest
from personality import PersonalityType
import json


def main(question_file='questions.json'):
    with open(question_file, 'r') as file:
        try:
            data = json.load(file)
            test = VoightKampffTest(data)
            if test.run() == PersonalityType.HUMAN:
                print('You are a human')
            else:
                print('You are a replicant')
        except json.JSONDecodeError:
            print(f'File \'{question_file}\' has an invalid format or is empty')


if __name__ == '__main__':
    main()
