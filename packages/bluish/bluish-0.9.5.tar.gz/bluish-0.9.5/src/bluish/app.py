import contextlib
import logging
import os
from io import StringIO
from typing import Never

import click
import yaml
from flask import Flask, abort, jsonify, request

from bluish.__main__ import PROJECT_VERSION
from bluish.core import (
    init_commands,
)
from bluish.nodes import WorkflowDefinition
from bluish.nodes.job import Job
from bluish.nodes.workflow import Workflow


class LogFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "white",
        logging.INFO: "bright_white",
        logging.WARNING: "yellow",
        logging.ERROR: "red",
        logging.CRITICAL: "bright_red",
    }

    def __init__(self, format: str) -> None:
        super().__init__(fmt=format)

    def format(self, record: logging.LogRecord) -> str:
        record.msg = click.style(
            record.msg, fg=self.COLORS.get(record.levelno, "white")
        )
        return super().format(record)


def fatal(message: str, exit_code: int = 1) -> Never:
    click.secho(message, fg="red", bold=True)
    exit(exit_code)


def init_logging(level_name: str) -> None:
    for level in [
        logging.INFO,
        logging.DEBUG,
        logging.WARNING,
        logging.ERROR,
        logging.CRITICAL,
    ]:
        logging.addLevelName(level, "")

    log_level = getattr(logging, level_name.upper(), logging.INFO)
    logging.basicConfig(level=log_level)
    logging.getLogger().handlers[0].setFormatter(
        LogFormatter("%(levelname)s%(message)s")
    )


def locate_yaml(name: str) -> str | None:
    """Locates the workflow file."""

    if not name:
        name = "bluish"

    paths = (name, f".bluish/{name}")
    exts = (".yaml", ".yml")

    for path in paths:
        for ext in exts:
            if os.path.exists(f"{path}{ext}"):
                return f"{path}{ext}"

    return None


def workflow_from_file(file: str) -> Workflow:
    """Loads the workflow from a file."""

    yaml_contents: str = ""

    with contextlib.suppress(FileNotFoundError):
        with open(file, "r") as yaml_file:
            yaml_contents = yaml_file.read()

    if not yaml_contents:
        fatal("No workflow file found.")

    definition = WorkflowDefinition(**yaml.safe_load(yaml_contents))
    return Workflow(definition)


@click.command("blu")
@click.argument("job_id", type=str, required=True)
@click.option("--no-deps", is_flag=True, help="Don't run job dependencies")
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"]),
    default="INFO",
    help="Log level",
)
@click.version_option(PROJECT_VERSION)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def blu_cli(
    job_id: str,
    no_deps: bool,
    log_level: str,
    args: tuple[str],
) -> None:
    init_logging(log_level)
    init_commands()

    file: str = ""
    if ":" in job_id:
        file, job_id = job_id.split(":")

    yaml_path = locate_yaml(file)
    if not yaml_path:
        fatal("No workflow file found.")

    logging.info(f"Loading workflow from {yaml_path}")
    logging.info("")

    wf = workflow_from_file(yaml_path)
    wf.set_inputs({k: v for k, v in (arg.split("=", maxsplit=1) for arg in args)})

    job: Job | None = wf.jobs.get(job_id)
    if not job:
        fatal(f"Job '{job_id}' not found.")

    try:
        result = wf.dispatch_job(job, no_deps)
        if result.failed:
            exit(result.returncode)
        else:
            click.secho("Job completed successfully.", fg="green")

    except Exception as e:
        if os.environ.get("BLUISH_DEBUG"):
            import traceback

            trace = traceback.format_exc()
            print(trace)
        fatal(str(e))


@click.group("bluish")
@click.option(
    "--file", "-f", type=click.Path(dir_okay=False, readable=True, resolve_path=True)
)
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"]),
    default="INFO",
    help="Log level",
)
@click.version_option(PROJECT_VERSION)
@click.pass_context
def bluish_cli(
    ctx: click.Context,
    file: str,
    log_level: str,
) -> None:
    init_logging(log_level)
    init_commands()

    yaml_contents: str = ""
    yaml_path = file or locate_yaml("")
    if not yaml_path:
        fatal("No workflow file found.")

    logging.info(f"Loading workflow from {yaml_path}")
    logging.info("")

    with contextlib.suppress(FileNotFoundError):
        with open(yaml_path, "r") as yaml_file:
            yaml_contents = yaml_file.read()

    if not yaml_contents:
        fatal("No workflow file found.")

    definition = WorkflowDefinition(**yaml.safe_load(yaml_contents))
    wf = Workflow(definition)
    ctx.obj = wf


@bluish_cli.command("list")
@click.pass_obj
def list_jobs(wf: Workflow) -> None:
    if not wf.jobs:
        fatal("No jobs found in workflow file.")

    items = tuple((id, job.attrs.name or "") for id, job in wf.jobs.items())
    id_len = max(len(id) for id, _ in items)

    click.secho(f"{'ID':<{id_len}}  NAME", fg="yellow", bold=True)
    for id, name in items:
        click.echo(f"{id:<{id_len}}  {name}")


@bluish_cli.command("run")
@click.argument("job_id", type=str, required=True)
@click.option("--no-deps", is_flag=True, help="Don't run job dependencies")
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
@click.pass_obj
def run_job(wf: Workflow, job_id: str, no_deps: bool, args: tuple[str]) -> None:
    wf.set_inputs({k: v for k, v in (arg.split("=", maxsplit=1) for arg in args)})
    job = wf.jobs.get(job_id)
    if not job:
        fatal(f"Job '{job_id}' not found.")

    try:
        result = wf.dispatch_job(job, no_deps)
        if result.failed:
            exit(result.returncode)
        else:
            click.secho("Job completed successfully.", fg="green")
    except Exception as e:
        if os.environ.get("BLUISH_DEBUG"):
            import traceback

            trace = traceback.format_exc()
            print(trace)

        fatal(str(e))


@bluish_cli.command("serve")
@click.argument(
    "workflow_path",
    type=click.Path(file_okay=False, dir_okay=True, exists=True),
    required=True,
)
@click.option("--host", type=str, default="localhost", help="Host")
@click.option("--port", type=int, default=5000, help="Port")
def serve(workflow_path: str, host: str, port: int) -> None:
    app = Flask(__name__)

    @app.route("/")
    def serve_index():
        return abort(404)

    @app.route("/<file>/<job_id>")
    def dispatch_job(file: str, job_id: str):
        file = f"{file}.yaml"
        if file not in os.listdir(workflow_path):
            return abort(404)

        wf = workflow_from_file(f"{workflow_path}/{file}")
        job = wf.jobs.get(job_id)
        if not job:
            return abort(404)

        log_level_name = request.args.get("log_level", "INFO")
        log_level = getattr(logging, log_level_name.upper(), logging.INFO)

        log_stream = StringIO()
        logging.basicConfig(
            stream=log_stream, level=log_level, format="%(message)s", force=True
        )

        result = wf.dispatch_job(job, False)

        return jsonify(
            {
                "run": result is not None,
                "stdout": log_stream.getvalue().splitlines(),
                "stderr": result.stderr if result else None,
                "returncode": result.returncode if result else None,
            }
        )

    app.run(host=host, port=port)


if __name__ == "__main__":
    pass
