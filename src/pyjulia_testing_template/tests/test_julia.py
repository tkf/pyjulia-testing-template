def test_julia(julia):
    assert julia.eval('1 + 1') == 2


def test_python():
    assert 1 + 1 == 2
