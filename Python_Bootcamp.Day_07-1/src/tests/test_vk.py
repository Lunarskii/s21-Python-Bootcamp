from voight_kampff_test import VoightKampffTest, PersonalityType
from .test_quiz import questions_from_file


def test_passed_only_humanity_test(questions_from_file, monkeypatch):
    input_data = ['2', '16', '100', '6', '8',
                  '1', '16', '100', '6', '8',
                  '2', '16', '100', '6', '8',
                  '2', '16', '100', '6', '8',
                  '3', '16', '100', '6', '8',
                  '4', '16', '100', '6', '8',
                  '1', '16', '100', '6', '8',
                  '2', '16', '100', '6', '8',
                  '1', '16', '100', '6', '8',
                  '1', '16', '100', '6', '8']
    monkeypatch.setattr('builtins.input', lambda x: input_data.pop(0))
    assert VoightKampffTest(questions_from_file).run() == PersonalityType.HUMAN


def test_passed_only_quiz(questions_from_file, monkeypatch):
    input_data = ['1', '12', '60', '1', '2',
                  '2', '12', '60', '1', '2',
                  '1', '12', '60', '1', '2',
                  '1', '12', '60', '1', '2',
                  '1', '12', '60', '1', '2',
                  '1', '12', '60', '1', '2',
                  '2', '12', '60', '1', '2',
                  '1', '12', '60', '1', '2',
                  '2', '12', '60', '1', '2',
                  '2', '12', '60', '1', '2']
    monkeypatch.setattr('builtins.input', lambda x: input_data.pop(0))
    assert VoightKampffTest(questions_from_file).run() == PersonalityType.HUMAN


def test_all_failed(questions_from_file, monkeypatch):
    input_data = ['2', '12', '60', '1', '2',
                  '1', '12', '60', '1', '2',
                  '2', '12', '60', '1', '2',
                  '2', '12', '60', '1', '2',
                  '3', '12', '60', '1', '2',
                  '4', '12', '60', '1', '2',
                  '1', '12', '60', '1', '2',
                  '2', '12', '60', '1', '2',
                  '1', '12', '60', '1', '2',
                  '1', '12', '60', '1', '2']
    monkeypatch.setattr('builtins.input', lambda x: input_data.pop(0))
    assert VoightKampffTest(questions_from_file).run() == PersonalityType.REPLICANT


def test_all_success(questions_from_file, monkeypatch):
    input_data = ['1', '16', '100', '6', '8',
                  '2', '16', '100', '6', '8',
                  '1', '16', '100', '6', '8',
                  '1', '16', '100', '6', '8',
                  '1', '16', '100', '6', '8',
                  '1', '16', '100', '6', '8',
                  '2', '16', '100', '6', '8',
                  '1', '16', '100', '6', '8',
                  '2', '16', '100', '6', '8',
                  '2', '16', '100', '6', '8']
    monkeypatch.setattr('builtins.input', lambda x: input_data.pop(0))
    assert VoightKampffTest(questions_from_file).run() == PersonalityType.HUMAN
