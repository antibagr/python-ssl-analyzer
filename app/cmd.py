import signal
import typing as t

import click

from app.services.service import analyze_service, application_dependencies


@click.group()
def cli() -> None:
    ...


def handle_exit_signal(_sig, _frame) -> t.NoReturn:
    raise SystemExit


@click.command()
def run() -> None:
    with application_dependencies():
        analyze_service.analyze()


cli.add_command(run)
signal.signal(signal.SIGINT, handle_exit_signal)
signal.signal(signal.SIGTERM, handle_exit_signal)

if __name__ == "__main__":
    cli()
