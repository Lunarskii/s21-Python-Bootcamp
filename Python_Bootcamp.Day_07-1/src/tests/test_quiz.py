from quiz import Quiz, PersonalityType
import pytest
import json


@pytest.fixture
def questions_from_file():
    with open('questions.json') as file:
        return json.load(file)


def test_all_replies_incorrect(questions_from_file, monkeypatch):
    input_data = ['2', '1', '2', '2', '3', '4', '1', '2', '1', '1']
    monkeypatch.setattr('builtins.input', lambda x: input_data.pop(0))
    assert Quiz(questions_from_file).run() == PersonalityType.REPLICANT


def test_all_replies_correct(questions_from_file, monkeypatch):
    input_data = ['1', '2', '1', '1', '1', '1', '2', '1', '2', '2']
    monkeypatch.setattr('builtins.input', lambda x: input_data.pop(0))
    assert Quiz(questions_from_file).run() == PersonalityType.HUMAN


def test_half_replies_correct(questions_from_file, monkeypatch):
    input_data = ['1', '2', '1', '1', '1', '4', '1', '2', '1', '1']
    monkeypatch.setattr('builtins.input', lambda x: input_data.pop(0))
    assert Quiz(questions_from_file).run() == PersonalityType.REPLICANT


def test_70_percent_replies_correct(questions_from_file, monkeypatch):
    input_data = ['1', '2', '1', '1', '1', '1', '2', '2', '1', '1']
    monkeypatch.setattr('builtins.input', lambda x: input_data.pop(0))
    assert Quiz(questions_from_file).run() == PersonalityType.HUMAN


def test_invalid_values(questions_from_file, monkeypatch):
    input_data = ['0', '5', '1', '2', '1', '1', '1', '1', '2', '1', '2', '2']
    monkeypatch.setattr('builtins.input', lambda x: input_data.pop(0))
    assert Quiz(questions_from_file).run() == PersonalityType.HUMAN


def test_invalid_type(questions_from_file, monkeypatch):
    input_data = ['test', '1', '2', '1', '1', '1', '1', '2', '1', '2', '2']
    monkeypatch.setattr('builtins.input', lambda x: input_data.pop(0))
    assert Quiz(questions_from_file).run() == PersonalityType.HUMAN
