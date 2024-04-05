from humanity_test import HumanityTest, PersonalityType


def test_min_replies(monkeypatch):
    input_data = ['12', '60', '1', '2']
    monkeypatch.setattr('builtins.input', lambda x: input_data.pop(0))
    assert HumanityTest().run() == PersonalityType.REPLICANT


def test_max_replies(monkeypatch):
    input_data = ['16', '100', '6', '8']
    monkeypatch.setattr('builtins.input', lambda x: input_data.pop(0))
    assert HumanityTest().run() == PersonalityType.HUMAN


def test_avg_replies(monkeypatch):
    input_data = ['14', '80', '3', '5']
    monkeypatch.setattr('builtins.input', lambda x: input_data.pop(0))
    assert HumanityTest().run() == PersonalityType.HUMAN


def test_invalid_values(monkeypatch):
    input_data = ['10', '12', '120', '60', '99', '1', '2']
    monkeypatch.setattr('builtins.input', lambda x: input_data.pop(0))
    assert HumanityTest().run() == PersonalityType.REPLICANT


def test_invalid_type(monkeypatch):
    input_data = ['test', '12', 'test', 'test', '60', '3.5', '3', '2']
    monkeypatch.setattr('builtins.input', lambda x: input_data.pop(0))
    assert HumanityTest().run() == PersonalityType.REPLICANT
