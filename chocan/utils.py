from enum import Enum
from pathlib import Path


class Alignment(Enum):
    Left = 0
    Center = 1
    Right = 2


def get_top_directory():
    return Path(__file__).parent.parent


def check_file(file: Path):
    """Check if the file and its path are valid to write to. If the path does
    not exist, create it.

    Args:
        file (Path): file to check

    Returns:
        bool: whether the file path is valid to write to
    """
    # First, check if the file's parent (directory) is a valid directory.
    if not file.parent.is_dir():
        # If it is not a directory and it exists, then it is not valid.
        if file.parent.exists():
            return False
        # If it is not a directory and it does not exist, it can be created.
        else:
            file.parent.mkdir(parents=True, exist_ok=True)

    # If the file exists and is not a file, it is not valid.
    if file.exists() and not file.is_file():
        return False

    # Otherwise, we can continue.
    return True


def confirmation(message):
    """Ask the user to confirm an action.

    Args:
        message (str): message to display to the user.

    Returns:
        bool: True if yes; False if no
    """
    confirm = input(f"{message} (y/n) ").lower().strip()
    return confirm == "yes" or confirm == "y"


def tabulate(col_names, row_tuples, col_alignments=[]):
    """Tabulate given data, print it, and return it.

    Args:
        col_names (list[str]): list of names to print for column headers
        row_tuples (list[tuple]): list of tuples to print as rows
        col_alignments (list, optional): alignments for each column's data.
            Defaults to [].

    Returns:
        str: generated table
    """
    text = ""
    column_lengths = []
    col_count = len(col_names)
    align_count = len(col_alignments)
    extra_chars = 0

    try:
        # Loop through the column names and print them
        for i in range(col_count):
            name_len = len(col_names[i])
            data_len = max([len(str(val[i])) for val in row_tuples])

            # Store the longest choice, column name length or data length
            column_lengths.append(name_len if name_len > data_len else data_len)

            text += f"{col_names[i].center(column_lengths[i])}"

            # Print a separator between names
            if i < col_count - 1:
                text += " | "
                extra_chars += 3

        # Print a separator
        text += "\n" + ("-" * (sum(column_lengths) + extra_chars)) + "\n"

        # Loop through the rows
        for i in range(len(row_tuples)):
            for j in range(col_count):
                # Determine which column alignment to use, default left
                if j > align_count - 1 or col_alignments[j] == Alignment.Left:
                    text += f"{str(row_tuples[i][j]).ljust(column_lengths[j])}"
                elif col_alignments[j] == Alignment.Center:
                    text += f"{str(row_tuples[i][j]).center(column_lengths[j])}"
                elif col_alignments[j] == Alignment.Right:
                    text += f"{str(row_tuples[i][j]).rjust(column_lengths[j])}"

                # Print a separator between each element
                if j < col_count - 1:
                    text += " | "

            text += "\n"

        return text
    except IndexError:
        print("Too many column names provided.")
        return ""
