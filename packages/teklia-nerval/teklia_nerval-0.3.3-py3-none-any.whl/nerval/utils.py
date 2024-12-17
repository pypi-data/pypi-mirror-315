from prettytable import MARKDOWN, PrettyTable

from nerval import ALL_ENTITIES

TABLE_HEADER = ["tag", "predicted", "matched", "Precision", "Recall", "F1", "Support"]


def print_markdown_table(header: list[str], rows: list[list]) -> list[list]:
    """Prints a Markdown table filled with the provided header and rows."""
    table = PrettyTable()
    table.field_names = header
    table.set_style(MARKDOWN)
    # Align all columns at right
    table.align = "r"
    # First column should be left aligned still
    table.align[header[0]] = "l"

    def _special_sort(row: list[str]) -> str:
        if row[0] == ALL_ENTITIES:
            # Place the line for all entities at the very top
            return ""
        return row[0]

    rows.sort(key=_special_sort)
    # Place ALL_ENTITIES row at the end
    rows.append(rows.pop(0))

    table.add_rows(rows)
    print(table)

    return rows


def print_results(scores: dict) -> list[list]:
    """Display final results.

    None values are kept to indicate the absence of a certain tag in either annotation or prediction.
    """
    results = []
    for tag in sorted(scores, reverse=True):
        prec = None if scores[tag]["P"] is None else round(scores[tag]["P"], 3)
        rec = None if scores[tag]["R"] is None else round(scores[tag]["R"], 3)
        f1 = None if scores[tag]["F1"] is None else round(scores[tag]["F1"], 3)

        results.append(
            [
                tag,
                scores[tag]["predicted"],
                scores[tag]["matched"],
                prec,
                rec,
                f1,
                scores[tag]["Support"],
            ],
        )

    return print_markdown_table(TABLE_HEADER, results)


def print_result_compact(scores: dict) -> list[list]:
    result = [
        ALL_ENTITIES,
        scores[ALL_ENTITIES]["predicted"],
        scores[ALL_ENTITIES]["matched"],
        round(scores[ALL_ENTITIES]["P"], 3),
        round(scores[ALL_ENTITIES]["R"], 3),
        round(scores[ALL_ENTITIES]["F1"], 3),
        scores[ALL_ENTITIES]["Support"],
    ]

    return print_markdown_table(TABLE_HEADER, [result])
