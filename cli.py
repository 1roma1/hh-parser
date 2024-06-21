import click

from src.parsing import Parser
from src.utils import load_configuration


@click.command()
def parse():
    config = load_configuration("config.yaml")
    parser = Parser(
        url_template=config["url_template"],
        headers=config["headers"],
        datadir=config["datadir"],
    )
    parser.run()
    parser.save_to_file()


@click.group()
def cli():
    pass


cli.add_command(parse)


if __name__ == "__main__":
    cli()
