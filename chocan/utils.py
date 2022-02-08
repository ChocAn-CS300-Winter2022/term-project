from pathlib import Path


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

    # TODO: If prompt does not ask for correct input, replace with:
    # return confirm == "yes" or confirm == "y"
    if confirm == "yes" or confirm == "y":
        return True
    elif confirm == "no" or confirm == "n":
        return False
    else:
        # TODO: Prompt for correct input or incorrect input returns False?
        print("Please enter one of these values: yes, no, y, n.")
        return confirmation(message)
