def test_julia(julia):
    assert julia.eval('1 + 1') == 2
