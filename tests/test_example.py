from othero import main


def test_main_outputs_hello(capsys):
    rc = main([])
    captured = capsys.readouterr()
    assert "Hello from othero!" in captured.out
    assert rc == 0
