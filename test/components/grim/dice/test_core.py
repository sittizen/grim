from grim.dice import d


def mock_randrange(start, stop):
    if not hasattr(mock_randrange, "last"):
        mock_randrange.last = start - 1
    mock_randrange.last += 1
    return mock_randrange.last


def test_mockrandrange():
    mock_randrange.last = 0
    assert mock_randrange(1, 6) == 1
    assert mock_randrange(1, 6) == 2
    assert mock_randrange(1, 6) == 3
    assert mock_randrange(1, 6) == 4
    assert mock_randrange(1, 6) == 5
    assert mock_randrange(1, 6) == 6


def test_d1():
    assert d(1) == 1
    assert d(1, adv=1) == 1
    assert d(1, dis=1) == 1
    assert d(1, adv=1, dis=1) == 1


def test_multiple_rolls(monkeypatch):
    assert d((1, 1, 1)) == 3

    monkeypatch.setattr("grim.dice.core.randrange", mock_randrange)
    mock_randrange.last = 0
    assert d((6, 6, 6)) == 1 + 2 + 3

    mock_randrange.last = 0
    assert d((6, 6, 6), adv=1) == 2 + 4 + 6


def test_adv_and_dis(monkeypatch):
    monkeypatch.setattr("grim.dice.core.randrange", mock_randrange)
    mock_randrange.last = 0
    assert d(6, adv=1) == 2

    mock_randrange.last = 0
    assert d(6, dis=1) == 1

    mock_randrange.last = 0
    assert d(6, adv=1, dis=1) == 1

    mock_randrange.last = 0
    assert d(6, adv=2, dis=1) == 2


def test_cap_low_and_high(monkeypatch):
    monkeypatch.setattr("grim.dice.core.randrange", mock_randrange)

    mock_randrange.last = 0
    assert d(6, capl=2) == 2

    mock_randrange.last = 0
    assert d(6, adv=5, caph=5) == 5
