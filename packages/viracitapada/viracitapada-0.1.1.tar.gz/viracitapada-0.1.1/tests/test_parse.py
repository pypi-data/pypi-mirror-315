import pytest

import viracitapada as vp


def test_parse():
    assert vp.parse_meter("yahvā́ iva prá vayā́m ujjíhānāḥ") == "—— ◡— ◡ ◡— —◡——"
    assert vp.parse_meter("kr̥tam") == "◡—"
    assert vp.parse_meter("górabhasam ádribhir vaatā́pyam") == "—◡◡◡ —◡— ◡◡——"
    assert vp.parse_meter("ví ā́śāḥ párvatānaam") == "◡ —— —◡—◡—"
    assert vp.parse_meter("yé asyā ̀ ācáraṇeṣu dadhriré") == "— —— · —◡◡—◡ —◡—"
    assert vp.parse_meter("úṣo yé te ̀ prá yā́meṣu yuñjáte") == "◡— — — · ◡ ——◡ —◡—"
    assert vp.parse_meter("kadā́ vaso ̀ stotráṁ háryate ā́") == "◡— ◡— · —— —◡— —"
    assert vp.parse_meter("íti krátvā nyeriré") == "◡— —— —◡—"
    assert vp.parse_meter("íti krátvā nieriré") == "◡— —— ◡—◡—"
    assert vp.parse_meter("tuvā́ṁ hí agne sádam ít samanyávo") == "◡— ◡ —— ◡◡ — ◡—◡—"


def test_parse_custom_marks():
    assert (
        vp.parse_meter(
            "kadā́ vaso ̀ stotráṁ háryate ā́",
            long_mark="L",
            short_mark="S",
            pause_mark="P",
        )
        == "SL SL P LL LSL L"
    )


def test_parse_invalid_type():
    with pytest.raises(TypeError):
        vp.parse_meter(False)


def test_parse_lines_multiline_str(
    rv_lines,
    rv_lines_parsed,
):
    lines_out = vp.parse_meter("\n".join(rv_lines))
    assert isinstance(lines_out, str)
    lines_out = lines_out.splitlines()
    assert len(lines_out) == 3
    for i in range(len(lines_out)):
        assert lines_out[i] == rv_lines_parsed[i]


def test_parse_lines_list_of_str(
    rv_lines,
    rv_lines_parsed,
):
    lines_out = vp.parse_meter(rv_lines)
    assert isinstance(lines_out, list)
    assert len(lines_out) == 3
    for i in range(len(lines_out)):
        assert lines_out[i] == rv_lines_parsed[i]


def test_parse_type_error():
    with pytest.raises(TypeError):
        vp.parse_meter(
            [
                "yahvā́ iva",
                1,
                True,
            ]
        )
