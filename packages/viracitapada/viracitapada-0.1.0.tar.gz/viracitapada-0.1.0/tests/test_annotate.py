import pytest

import viracitapada as vp


def test_annotate(
    rv_lines,
    rv_lines_annotated,
):
    for i in range(len(rv_lines)):
        assert vp.annotate_metrical_pos(rv_lines[i]) == rv_lines_annotated[i]


def test_annotate_lines_multiline_str(
    rv_lines,
    rv_lines_annotated,
):
    lines_out = vp.annotate_metrical_pos("\n".join(rv_lines))
    assert isinstance(lines_out, str)
    lines_out = lines_out.splitlines()
    assert len(lines_out) == 3
    for i in range(len(lines_out)):
        assert lines_out[i] == rv_lines_annotated[i]


def test_annotate_lines_list_of_str(
    rv_lines,
    rv_lines_annotated,
):
    lines_out = vp.annotate_metrical_pos(rv_lines)
    assert isinstance(lines_out, list)
    assert len(lines_out) == 3
    for i in range(len(lines_out)):
        assert lines_out[i] == rv_lines_annotated[i]


def test_annotate_type_error():
    with pytest.raises(TypeError):
        vp.annotate_metrical_pos(
            [
                "yahvā́ iva",
                1,
                True,
            ]
        )
