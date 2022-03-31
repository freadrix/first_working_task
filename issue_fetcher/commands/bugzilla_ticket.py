import click

from issue_fetcher.service import fetcher_tickets


@click.command()
def cli():
    """Fetch Fedora tickets"""
    result = fetcher_tickets.fetch_bugs()
    print(result)
    print(len(result))
