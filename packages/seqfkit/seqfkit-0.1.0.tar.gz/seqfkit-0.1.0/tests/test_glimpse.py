'''
Author: Chou_Uken Chouuken@outlook.com
Date: 2024-12-15 22:33:09
LastEditors: Chou_Uken Chouuken@outlook.com
LastEditTime: 2024-12-15 22:34:13
FilePath: /seqfkit/seqfkit/test_glimpse.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import pytest
from click.testing import CliRunner
from seqfkit.utils import glimpse

@pytest.fixture
def runner():
    return CliRunner()

def test_glimpse_with_valid_fasta(runner):
    result = runner.invoke(glimpse, ['--fasta_file', 'tests/data/valid.fasta'])
    assert result.exit_code == 0
    assert 'Sequence Number:' in result.output

def test_glimpse_with_invalid_fasta(runner):
    result = runner.invoke(glimpse, ['--fasta_file', 'tests/data/invalid.fasta'])
    assert result.exit_code != 0

def test_glimpse_with_verbose(runner):
    result = runner.invoke(glimpse, ['--fasta_file', 'tests/data/valid.fasta', '--verbose'])
    assert result.exit_code == 0
    assert 'Sequence Number:' in result.output
    assert 'Contains:' in result.output
