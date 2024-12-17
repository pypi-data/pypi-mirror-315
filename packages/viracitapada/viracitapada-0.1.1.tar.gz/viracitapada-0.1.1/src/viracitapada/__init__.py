import re

from typing import Literal, get_args
from unicodedata import normalize


# Type aliases
Normalization = Literal["NFC", "NFKC", "NFD", "NFKD"]
InputType = Literal["str", "multiline_str", "list"]

# default long/short/pause marks
_LONG = "—"
_SHORT = "◡"
_PAUSE = "·"

# whitespace supplements
_SPC_PAT = r"\s+"
_SPC_MARK = "_"
_SPC_OPT_MARK = _SPC_MARK + "?"

# matching vowels
_VL_PAT = r"(ā|ī|ū|o|e|ai|au)"
_VS_PAT = r"(a|i|u|r̥|l̥)"

# meta chars
_METAS_PAT = r"[ ̥]"

# matching and marking consonants
_C_SINGLE_PAT = (
    r"(?!(a|i|u|r̥|l̥|\s|"
    + _METAS_PAT
    + "|"
    + _SHORT
    + "|"
    + _LONG
    + "|"
    + _PAUSE
    + "))."
)
_C_DOUBLE_PAT = r"(ph|th|kh|bh|dh|gh|jh)"
_C_MARK = "#"

# matching metrical pause
_MP_PAT = r"\s\u0300"  # space(s) followed by gravis: " ̀ "


def _validate_input(lines: str | list[str]) -> tuple[InputType, list[str]]:
    input_type = None
    if isinstance(lines, str):
        input_type = get_args(InputType)[0]
        if "\n" in lines:
            input_type = get_args(InputType)[1]
        lines = lines.splitlines()
    elif isinstance(lines, list) and all(isinstance(line, str) for line in lines):
        input_type = get_args(InputType)[2]
    else:
        raise TypeError("Input line(s) must be of type str or list[str]")
    return input_type, lines


def _clean(string: str) -> str:
    """
    Cleans a string from acute accents (´) as well as "-", "=", "/", "\\", "?" and "_"
    """
    text = normalize("NFD", string)
    text = re.sub(r"[\u0301\u0027\-+=_/\?\\]", "", text)
    text = re.sub(r"(\S)\u0300", "\1", text)
    return normalize("NFC", text)


def _parse_meter(
    text: str,
    *,
    long_mark: str = _LONG,
    short_mark: str = _SHORT,
    pause_mark: str = _PAUSE,
) -> str:
    # clean string from unwanted chars and diacritics
    text = _clean(text)

    # mark metrical pauses (space with gravis in e.g. VN&H) as _PAUSE
    text = re.sub(
        _MP_PAT,
        _PAUSE,
        text,
    )

    # mark long vowels as _LONG
    text = re.sub(
        _VL_PAT,
        _LONG,
        text,
    )

    # mark consonants with double char notation
    text = re.sub(
        _C_DOUBLE_PAT,
        _C_MARK,
        text,
    )

    # mark remaining consonants
    text = re.sub(
        _C_SINGLE_PAT,
        _C_MARK,
        text,
    )

    # mark whitespaces
    text = re.sub(
        _SPC_PAT,
        _SPC_MARK,
        text,
    )

    # mark short vowels followed by any another vowel as _SHORT
    text = re.sub(
        _VS_PAT + "(?=" + _VS_PAT + "|" + _VL_PAT + ")",
        _SHORT,
        text,
    )

    # mark short vowels at line end as _SHORT
    text = re.sub(
        _VS_PAT + "$",
        _SHORT,
        text,
    )

    # mark short vowels at word end followed by vowel as _SHORT
    text = re.sub(
        _VS_PAT + "(?=" + _SPC_MARK + "[^" + _C_MARK + _PAUSE + "]" + ")",
        _SHORT,
        text,
    )

    # mark short vowels in last syllable of line as _LONG
    text = re.sub(
        _VS_PAT + _C_MARK + "+$",
        _LONG,
        text,
    )

    # mark short vowels followed by two consonants as _LONG
    text = re.sub(
        _VS_PAT + "(?=" + _SPC_OPT_MARK + _C_MARK + _SPC_OPT_MARK + _C_MARK + ")",
        _LONG,
        text,
    )

    # mark short vowels followed by one consonant as _SHORT
    text = re.sub(
        _VS_PAT
        + "(?="
        + _SPC_OPT_MARK
        + _C_MARK
        + ")(?!="
        + _SPC_OPT_MARK
        + _C_MARK
        + _PAUSE
        + ")",
        _SHORT,
        text,
    )

    # mark any remaining short vowels as _SHORT
    text = re.sub(
        _VS_PAT,
        _SHORT,
        text,
    )

    # remove all but metrical and and whitespace marks
    text = re.sub(
        "[^" + _LONG + _SHORT + _PAUSE + _SPC_MARK + "]",
        "",
        text,
    )

    # replace whitespace marks by actual whitespaces
    text = re.sub(
        _SPC_MARK + "+",
        " ",
        text,
    )

    # pad pause markers
    text = re.sub(
        r"\s*" + _PAUSE + r"\s*",
        " " + _PAUSE + " ",
        text,
    )

    # replace metrical marks
    if long_mark != _LONG:
        text = re.sub(_LONG, long_mark, text)
    if short_mark != _SHORT:
        text = re.sub(_SHORT, short_mark, text)
    if pause_mark != _PAUSE:
        text = re.sub(_PAUSE, pause_mark, text)

    return text


def parse_meter(
    lines: str | list[str],
    *,
    long_mark: str = _LONG,
    short_mark: str = _SHORT,
    pause_mark: str = _PAUSE,
) -> str | list[str]:
    r"""
    Parses an ISO-15919-transliterated Sanskrit string into a metrical notation with
    long/short syllable marks.

    If a mark string has a length greater than 1,
    it will be trimmed to the first character.

    vp.parse_meter("agním īḷe puróhitaṁ")
    # —◡ —— ◡—◡—

    This function will return the same type of data you passed to it,
    which can be either a single line of text as a `str` (`"line one"`),
    multiple lines of text as a `str` (`"line one\nline two\nline three"`)
    or a `list[str]` containing a line of text per string
    (`["line one", "line two", "line three"]`).
    Any other type of data will raise a `TypeError` and any different way of
    organizing lines of text in a `str` (e.g. a `list[str]` with multiline strings)
    will lead to undefined behaviour.
    """

    input_type, lines = _validate_input(lines)

    # determine long/short/pause marks to use for output
    long_mark = long_mark[:1] if long_mark else _LONG
    short_mark = short_mark[:1] if short_mark else _SHORT
    pause_mark = pause_mark[:1] if pause_mark else _PAUSE

    lines = [
        _parse_meter(
            line,
            long_mark=long_mark,
            short_mark=short_mark,
            pause_mark=pause_mark,
        )
        for line in lines
    ]

    if input_type == "list":
        return lines
    elif len(lines) == 1:
        return lines[0]
    else:
        return "\n".join(lines)


def _annotate_metrical_pos(
    line: str,
    normalization: Normalization = "NFC",
) -> str:
    tokens: list[str] = re.split(_SPC_PAT, line)
    tokens_parsed: list[str] = re.split(_SPC_PAT, str(parse_meter(line)))
    positions: list[int] = [0] * len(tokens_parsed)

    # compute positions
    for i in range(len(positions)):
        if i == 0:
            positions[i] = 1
        else:
            positions[i] = positions[i - 1] + len(tokens_parsed[i - 1])
        tokens[i] = str(positions[i]) + "_" + tokens[i]

    return normalize(normalization, " ".join(tokens))


def annotate_metrical_pos(
    lines: str | list[str],
    *,
    normalization: Normalization = "NFC",
) -> str | list[str]:
    r"""
    Annotates the tokens of lines of text with their metrical position.

    vp.annotate_metrical_pos("agním īḷe puróhitaṁ")
    # 1_agním 3_īḷe 5_puróhitaṁ

    This function will return the same type of data you passed to it,
    which can be either a single line of text as a `str` (`"line one"`),
    multiple lines of text as a `str` (`"line one\nline two\nline three"`)
    or a `list[str]` containing a line of text per string
    (`["line one", "line two", "line three"]`).
    Any other type of data will raise a `TypeError` and any different way of
    organizing lines of text in a `str` (e.g. a `list[str]` with multiline strings)
    will lead to undefined behaviour.
    """
    input_type, lines = _validate_input(lines)

    lines = [
        _annotate_metrical_pos(
            line,
            normalization,
        )
        for line in lines
    ]

    if input_type == "list":
        return lines
    elif len(lines) == 1:
        return lines[0]
    else:
        return "\n".join(lines)
