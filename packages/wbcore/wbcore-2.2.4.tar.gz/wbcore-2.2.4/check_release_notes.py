import glob
from pathlib import Path

from wbcore.release_notes.utils import parse_release_note

if __name__ == "__main__":
    base_path = "../"
    errors = {}
    for release_note_folder in [
        *glob.glob(f"{base_path}**/**/release_notes"),
        "wbcore/release_notes/release_notes",
        "wbcore/release_notes/frontend_release_notes",
    ]:
        if release_note_folder != "../wbcore/wbcore/release_notes":
            for release_note in Path(release_note_folder).iterdir():
                if not release_note.is_dir():
                    with open(release_note, "r") as markdown_file:
                        try:
                            parse_release_note(markdown_file.read())
                        except Exception as e:
                            errors[str(release_note).replace("../", "")] = e

    if errors:
        raise ValueError(f"These release notes trigger an error {errors}")
    else:
        print("ok")  # noqa: T201
