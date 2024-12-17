# viracitapada

![Tests Status](https://img.shields.io/github/actions/workflow/status/VedaWebProject/viracitapada/tests.yml?label=tests)
[![Tests Coverage](https://img.shields.io/coverallsCoverage/github/VedaWebProject/viracitapada?branch=main&label=tests%20coverage)](https://coveralls.io/github/VedaWebProject/viracitapada?branch=main)
![mypy](https://img.shields.io/badge/type%20checked-mypy-039dfc)


Performs metrical analysis on ISO-15919-transliterated Sanskrit verses.


## Features

- usable as a **library** in arbitrary projects (no CLI included, yet)
- **parses** lines of text into a **metrical notation** of long/short markers via `parse_meter` (see examples below)
- **annotates** the tokens of lines of text with their **metrical position** via `annotate_metrical_pos` (see examples below)


> [!NOTE]
> The way this library is implemented is quite naive – it uses simple string replacements matching regular expressions. This is (widely known to be) not the fastest approach to parsing things and while it probably won't be a problem in one-off applications like data transformation scripts or pipelines, it might show if used in user-facing applications that process very large amounts of data. The operations that are performed are still _very trivial_, so to find out if the performance is good enough for your use case, you should just give it a try.


## Usage

`parse_meter` as well as `annotate_metrical_pos` will return the same type of data you threw at them. This can be either a single line of text as a `str` (`"line one"`), multiple lines of text as a `str` (`"line one\nline two\nline three"`) or a `list[str]` containing a line of text per string (`["line one", "line two", "line three"]`).

Some examples:

```py
import viracitapada as vp

vp.parse_meter("agním īḷe puróhitaṁ")
# —◡ —— ◡—◡—

vp.parse_meter("úṣo yé te ̀ prá yā́meṣu yuñjáte")
# ◡— — — · ◡ ——◡ —◡— (" `" as pause)

vp.parse_meter(
    "kadā́ vaso ̀ stotráṁ háryate ā́",
    long_mark="L",
    short_mark="S",
    pause_mark="P",
)
# "SL SL P LL LSL L"

vp.parse_meter("agním īḷe puróhitaṁ\nyajñásya devám r̥tvíjam\nhótāraṁ ratnadhā́tamam")
# —◡ —— ◡—◡—\n——◡ —◡ —◡—\n——— —◡—◡—

vp.parse_meter([
    "agním īḷe puróhitaṁ",
    "yajñásya devám r̥tvíjam",
    "hótāraṁ ratnadhā́tamam",
])
# ["—◡ —— ◡—◡—", "——◡ —◡ —◡—", "——— —◡—◡—"]

vp.annotate_metrical_pos("agním īḷe puróhitaṁ")
# 1_agním 3_īḷe 5_puróhitaṁ

vp.annotate_metrical_pos(
    "agním īḷe puróhitaṁ\nyajñásya devám r̥tvíjam\nhótāraṁ ratnadhā́tamam"
)
# 1_agním 3_īḷe 5_puróhitaṁ\n1_yajñásya 4_devám 6_r̥tvíjam\n1_hótāraṁ 4_ratnadhā́tamam

vp.annotate_metrical_pos([
    "agním īḷe puróhitaṁ",
    "yajñásya devám r̥tvíjam",
    "hótāraṁ ratnadhā́tamam",
])
# ["1_agním 3_īḷe 5_puróhitaṁ", "1_yajñásya 4_devám 6_r̥tvíjam", "1_hótāraṁ 4_ratnadhā́tamam"]
```


## Development

This project uses [uv](https://docs.astral.sh/uv/) to manage dependencies.
Install uv to make use of the following commands.

Install library and dependencies in a local virtual environment:
```sh
uv sync
```

Check code formatting, run linter:
```sh
uv run ruff format . --check
uv run ruff check .
```

Format code and fix linter errors:
```sh
uv run ruff format .
uv run ruff check . --fix
```

Run mypy to check typing:
```sh
uv run mypy
```

Run tests and measure test coverage:
```sh
uv run coverage run -m pytest
```

Run specific tests file:
```sh
uv run coverage run -m pytest tests/test_clean.py
```

Print coverage report of last measured test run:
```sh
uv run coverage report -m
```

Run everything from above to make sure things are working and in good shape (on Unix-like systems):
```sh
./pre-commit.sh
```
