import pytest


@pytest.fixture(scope="session")
def rv_lines():
    return [
        "agním īḷe puróhitaṁ",
        "yajñásya devám r̥tvíjam",
        "hótāraṁ ratnadhā́tamam",
    ]


@pytest.fixture(scope="session")
def rv_lines_parsed():
    return [
        "—◡ —— ◡—◡—",
        "——◡ —◡ —◡—",
        "——— —◡—◡—",
    ]


@pytest.fixture(scope="session")
def rv_lines_annotated():
    return [
        "1_agním 3_īḷe 5_puróhitaṁ",
        "1_yajñásya 4_devám 6_r̥tvíjam",
        "1_hótāraṁ 4_ratnadhā́tamam",
    ]
