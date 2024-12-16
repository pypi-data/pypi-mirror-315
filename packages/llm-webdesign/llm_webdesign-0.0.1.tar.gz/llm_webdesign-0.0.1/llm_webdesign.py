import http.server
import os
import shutil
import socketserver
import tempfile
import threading
import webbrowser
from functools import partial
from pathlib import Path

import click
import llm
from llm.cli import get_default_model

# TODO: start from a URL e.g. --url=https://missas.com.br/ downloads the code
#       and save to the temp folder. can't be used with --in-place
# TODO: chat


# TODO: improve prompt
# TODO: make customizable
SYSTEM_PROMPT = """
You are a Web Designer.
You should prioritize the code (HTML, CSS, and JS) in your response.
Everything inside the ``` delimiters will be considered as code.
All code you output will be served to the user.
Do NOT return the tree of the project.
Return ONLY the index.html. All CSS and JS should be inside this file.
"""
PORT = 9876  # TODO: receive as CLI arg
CODE_DELIMITER = "```"


class QuietHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args, **kwargs):
        pass


def run_server(directory):
    os.chdir(directory)
    Handler = QuietHTTPRequestHandler
    # TODO: parametrize host
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()


def start_server(directory):
    # TODO: kill after finishing script
    server_thread = threading.Thread(target=run_server, args=(directory,), daemon=True)
    server_thread.start()


def parse(chunks, text_callback, code_callback, code_delimiter=CODE_DELIMITER):
    # TODO: refactor this crazy logic
    code = False
    current_line = ""
    for chunk in chunks:
        if current_line.endswith("\n"):
            # TODO: remove hard coded `
            if code and "`" in current_line and code_delimiter not in current_line:
                code_callback(current_line)
            current_line = ""
        current_line += chunk
        if code_delimiter in chunk or code_delimiter in current_line:
            # TODO: fix this for cases when the chunk contains more than ```
            code = not code
            continue
        if "`" in current_line:
            continue

        callback = code_callback if code else text_callback
        callback(chunk)


def write(f, chunk):
    f.write(chunk)
    f.flush()


def format_prompt(user_input, file_content):
    return f"""\
{user_input}

```
{file_content}
```"""


@llm.hookimpl
def register_commands(cli):
    @cli.command(context_settings={"ignore_unknown_options": True})
    @click.option(
        "--filename",
        default="index.html",
        help="The file that will be sent to the LLM and where the output will be written.",
    )
    @click.option("--path", help="Path to the directory with the files")
    @click.option(
        "--in-place",
        default=False,
        is_flag=True,
        help="Overwrite the files in the <path> instead of create a temporary directory.",
    )
    @click.argument("args", nargs=-1, type=click.UNPROCESSED)
    def webdesign(args, filename, path, in_place):
        path = Path(path)
        directory = path if in_place else Path(tempfile.mkdtemp())
        click.echo(f"Your files will be in the directory: {directory}")
        if not in_place:
            click.echo(f"Copying from {path} to {directory}")
            shutil.copytree(path, directory, dirs_exist_ok=True)
        start_server(directory)
        url = f"http://localhost:{PORT}"
        assert webbrowser.open(url)
        click.echo(f"Serving files at {url}")

        model = llm.get_model(get_default_model())
        if model.needs_key:
            model.key = llm.get_key(None, model.needs_key, model.key_env_var)

        with open(path / filename) as f:
            index_content = f.read()

        prompt = format_prompt("".join(args), index_content)
        response = model.prompt(prompt, system=SYSTEM_PROMPT)

        filepath = directory / filename

        with open(filepath, "w") as f:
            f.write("")

        my_print = partial(print, end="")

        with open(filepath, "a") as f:
            my_write = partial(write, f)
            parse(response, my_print, my_write)

        input("Press Enter to finish.")
