from main import main as program


def test_empty_file(capsys):
    file_name = 'empty.json'
    program(file_name)
    captured = capsys.readouterr()
    assert captured.out == f'File \'{file_name}\' has an invalid format or is empty\n'
