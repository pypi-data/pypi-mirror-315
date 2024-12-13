# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Module defining custom qBraid IPython magic commands.

"""

import os
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Optional

from IPython.core.magic import Magics, line_magic, magics_class

from qbraid_core.services.chat.client import ChatClient

LANGUAGES = [
    "python",
    "qasm",
    "javascript",
    "java",
    "c",
    "c++",
    "c#",
    "ruby",
    "php",
    "go",
    "swift",
    "kotlin",
    "rust",
    "typescript",
    "html",
    "css",
    "sql",
    "bash",
    "powershell",
    "yaml",
    "json",
    "xml",
    "markdown",
    "r",
    "matlab",
    "perl",
    "scala",
    "haskell",
    "lua",
    "dart",
    "groovy",
    "objective-c",
    "vb.net",
    "f#",
    "clojure",
    "erlang",
    "elixir",
    "ocaml",
    "julia",
    "lisp",
    "prolog",
    "fortran",
    "pascal",
    "cobol",
    "assembly",
    "latex",
    "graphql",
    "dockerfile",
    "makefile",
    "cmake",
    "vimscript",
    "vim",
    "tex",
]


def strip_code_fence(s: str) -> str:
    """
    Strips leading and trailing Markdown code fences from a string.

    Supports leading fences like ```python, ```qasm, or ``` with or without a language specifier.

    Args:
        s (str): The input string.

    Returns:
        str: The string without leading and trailing code fences if they exist.
    """
    if not (s.startswith("```") and s.endswith("```")):
        return s

    matched_lang = None
    for lang in LANGUAGES:
        if s.startswith(f"```{lang}"):
            matched_lang = lang
            break

    matched_lang = matched_lang or ""
    s = s.removeprefix(f"```{matched_lang}")
    s = s.removesuffix("```")

    return s.strip()


@magics_class
class SysMagics(Magics):
    """
    Custom IPython Magics class to allow running
    qBraid-CLI commands from within Jupyter notebooks.

    """

    @staticmethod
    def restore_env_var(var_name: str, original_value: Optional[str]) -> None:
        """
        Restore or remove an environment variable based on its original value.
        """
        if original_value is None:
            os.environ.pop(var_name, None)
        else:
            os.environ[var_name] = original_value

    @line_magic
    def qbraid(self, line):
        """
        Executes qBraid-CLI command using the sys.executable
        from a Jupyter Notebook kernel.
        """
        original_path = os.getenv("PATH")
        original_show_progress = os.getenv("QBRAID_CLI_SHOW_PROGRESS")
        python_dir = str(Path(sys.executable).parent)

        try:
            os.environ["PATH"] = python_dir + os.pathsep + original_path
            os.environ["QBRAID_CLI_SHOW_PROGRESS"] = "false"

            command = ["qbraid"] + shlex.split(line)
            if (
                len(command) == 5
                and command[1] == "chat"
                and command[2] in {"--format", "-f"}
                and command[3] == "code"
            ):
                response_format = command[3]
                prompt = command[-1]

                client = ChatClient()

                content = client.chat(prompt, response_format=response_format)

                code = strip_code_fence(content)

                self.shell.set_next_input(code)

            else:
                subprocess.run(command, check=True)

        finally:
            self.restore_env_var("PATH", original_path)
            self.restore_env_var("QBRAID_CLI_SHOW_PROGRESS", original_show_progress)


def load_ipython_extension(ipython):
    """Load the extension in IPython."""
    ipython.register_magics(SysMagics)
