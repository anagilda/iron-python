"""
Provide commands to interact with the iron algorith through the command line.
"""
import click

from algorithm.iron import Iron


@click.command()
@click.option('--unseal', 'sealed_string', help='Unseal the provided string.')
def iron_command(sealed_string):
    """
    Call the iron algorithm implementation as a command line command.
    """
    if sealed_string:
        click.echo(f'Unsealing "{sealed_string}"!')
        iron = Iron(password='ee%(u2d#&Zz#+.k4.W.2tR:RC2^y5h{%')
        iron.unseal(sealed=sealed_string)
