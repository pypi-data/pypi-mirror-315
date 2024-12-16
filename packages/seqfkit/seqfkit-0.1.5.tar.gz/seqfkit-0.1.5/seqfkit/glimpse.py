'''
Author: Chou_Uken Chouuken@outlook.com
Date: 2024-12-15 19:21:57
LastEditors: Chou_Uken Chouuken@outlook.com
LastEditTime: 2024-12-16 09:58:25
FilePath: /seqfkit/seqfkit/outline.py
Description: This script provides an overview of a FASTA file.
'''

import click
from .utils import read_fasta


@click.command()
@click.option('--fasta_file', '-f', required=True, type=click.Path(exists=True), prompt='Your FASTA file', help='The path of FASTA file.')
@click.option('--verbose', '-v', is_flag=True, default=False, help='Enable verbose output.')
def glimpse(fasta_file: click.Path, verbose: bool) -> None:
    seq_list: dict = read_fasta(file_path=fasta_file)
    click.echo('Sequence Number: {0}\n'.format(str(len(seq_list))))
    click.echo('Contains: {0}'.format(', '.join(['\'' + i + '\'' for i in seq_list.keys()])))


if __name__ == '__main__':
    glimpse()
