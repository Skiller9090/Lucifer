from termcolor import colored


def generate_table(array2d, title="", headings=None):
    if headings is None:
        headings = []
    out = ""
    max_char = -1
    max_cols = -1
    if len(headings) > 0:
        array2d.insert(0, headings)
    for line in array2d:
        max_cols = max(len(line), max_cols)
        for cell in line:
            cellLines = cell.split("\n")
            for string in cellLines:
                max_char = max(len(str(string)), max_char)
    title_total = (max_char * max_cols) + (max_cols - 1) - len(str(title))
    if title_total < 0:
        max_char = int(round(len(str(title)) / max_cols))
        title_total = (max_char * max_cols) + (max_cols - 1) - len(str(title))
    b_title, a_title = title_total // 2, title_total - (title_total // 2)
    dash_column = "—" * max_char
    if title != "":
        out += f'┌{"—" * ((max_char * max_cols) + (max_cols - 1))}┐\n'
        out += f'│{" " * b_title}{colored(title, "green", attrs=["bold"])}{" " * a_title}│\n'
        out += f'├{"┬".join(([dash_column] * max_cols))}┤\n'
    else:
        out += f'┌{"┬".join(([dash_column] * max_cols))}┐\n'
    for i, line in enumerate(array2d):
        while len(line) < max_cols:
            line.append("")
        depth = 1
        dataCells = []
        for data in line:
            nl_count = data.count("\n") + 1
            depth = nl_count if nl_count > depth else depth
            dataCells.append(data.split("\n"))
        for v in dataCells:
            while len(v) < depth:
                v.append("")
        for c, cellsLine in enumerate(zip(*dataCells)):
            out += "│" if c == 0 else "\n│"
            for cell in cellsLine:
                total = max_char - len(str(cell))
                before, after = total // 2, total - (total // 2)
                if len(headings) > 0 and i == 0:
                    cell = colored(cell, "blue", attrs=[])
                out += f"{' ' * before}{cell}{' ' * after}│"
        out += f'\n├{"┼".join(([dash_column] * max_cols))}┤\n' \
            if i != len(array2d) - 1 else "\n"
    out += f'└{"┴".join(([dash_column] * max_cols))}┘\n'
    return out
