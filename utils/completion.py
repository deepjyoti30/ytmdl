#!/usr/bin/env python3
"""Build the completion files

The arguments can be fetched by using the ytmdl
command.
"""
from subprocess import Popen, PIPE
from os import environ
from pathlib import Path


SHELLS_SUPPORTED = [
    "bash",
    "zsh"
]
DEFAULT_TEMPLATE = "ytmdl-{}-completion.in"
FINAL_NAME = "ytmdl.{}"


def build_files():
    """Build the files"""
    environ["PYTHONPATH"] = "./ytmdl"
    process = Popen(
        "python3 -m main --get-opts".split(), stdout=PIPE, stderr=PIPE)
    out, err = process.communicate()

    opts = out.decode("utf-8").replace("\n", "")

    for shell in SHELLS_SUPPORTED:
        template_name = DEFAULT_TEMPLATE.format(shell)
        template = open(Path("utils").joinpath(template_name)).read()

        # Update the ytmdl_opts with the opts
        template = template.replace("{{ytmdl_opts}}", opts)

        with open(FINAL_NAME.format(shell), "w") as w:
            w.write(template)


build_files()
