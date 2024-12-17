"""This file is part of pyphd.

pyphd is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyphd is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pyphd.  If not, see <https://www.gnu.org/licenses/>.

Copyright (C) 2024  phdenzel
"""

from pathlib import Path
from pyphd.parser import parse_args
from pyphd.template import PROJECT_STRUCTURE, FILE_HEADER


def main():
    """Main pyphd package method."""
    context = parse_args()
    verbose = context.pop("verbose", False)
    file_head = FILE_HEADER.format(**context)

    for fyle, content in PROJECT_STRUCTURE.items():
        fyle = Path(fyle.format(**context))
        content = content.format(**context)

        # write new file (and folders)
        if not fyle.exists():
            if verbose:
                print("Creating file:", fyle)
            fyle.parent.mkdir(parents=True, exist_ok=True)
            if not fyle.parent.samefile("."):
                with fyle.open("w") as f:
                    f.write(file_head)
                    f.write(content)
            else:
                with fyle.open("w") as f:
                    f.write(content)
        # add file header to project files if missing
        elif not fyle.parent.samefile("."):
            with fyle.open("r+") as f:
                text = fyle.read_text()
                if not text.startswith(file_head):
                    if verbose:
                        print("Amending file:", fyle)
                    f.seek(0)
                    f.writelines(file_head + text)
