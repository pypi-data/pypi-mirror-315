"""This file is part of pyphd. It implements a config parser.

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

import os
import datetime
from argparse import ArgumentParser
from dotenv import dotenv_values


def parse_args(**kwargs) -> dict:
    """Parse arguments."""
    parser = ArgumentParser()

    # fetch environment variables from .env file
    env_map = {
        "PYPHD_PKG_NAME": "pkg_name",
        "PYPHD_NAME": "name",
        "PYPHD_EMAIL": "email",
        "PYPHD_USERNAME": "user_name",
    }
    dot_kwargs = dotenv_values()
    for k in dot_kwargs.copy():
        if k in env_map and env_map[k] not in kwargs:
            kwargs[env_map[k]] = dot_kwargs.pop(k)

    # options
    parser.add_argument("-v", "--verbose", action="store_true", help="Set verbosity.")
    parser.add_argument(
        "-p",
        "--pkg-name",
        "--pkg",
        "--pkg_name",
        type=str,
        default=kwargs.get("pkg_name", "project_template"),
        help="Package name.",
    )
    parser.add_argument(
        "-n",
        "--name",
        type=str,
        default=kwargs.get("name", os.environ["USER"]),
        help="Name of the author/maintainer.",
    )
    parser.add_argument(
        "-e",
        "--email",
        type=str,
        default=kwargs.get("email", f"{os.environ['USER']}@py.dev"),
        help="Email of the author/maintainer.",
    )
    parser.add_argument(
        "-u",
        "--user_name",
        "--username",
        "--user",
        type=str,
        default=kwargs.get("username", f"{os.environ['USER']}"),
        help="Username of the author/maintainer.",
    )
    parser.add_argument(
        "-y",
        "--year",
        type=str,
        default=kwargs.get("year", str(datetime.datetime.now().year)),
        help="The (current) year.",
    )

    # convert parsed arguments into dictionary
    args, _ = parser.parse_known_args()
    context = vars(args)
    return context


if __name__ == "__main__":
    context = parse_args()
    print(context)
