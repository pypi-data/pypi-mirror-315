import viracitapada as vp


def test_clean_1():
    assert vp._clean("agním īḷe puróhitaṁ") == "agnim īḷe purohitaṁ"


def test_clean_2():
    assert vp._clean("ag-ním= īḷe/ puróhi\\ta?ṁ") == "agnim īḷe purohitaṁ"
