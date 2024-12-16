'''
Author: Chou_Uken Chouuken@outlook.com
Date: 2024-12-13 14:33:47
LastEditors: Chou_Uken Chouuken@outlook.com
LastEditTime: 2024-12-14 18:20:43
FilePath: /seqfkit/tests/test_utils.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import pytest
import os
from seqfkit.utils import read_fasta, read_first_fasta, complement


@pytest.fixture
def fasta_file():
    fasta_content = ">seq1\nATGCGTA\n>seq2\nCGTACGTAGCTA\n>seq3\nGCTAGCTAGCTA"
    fasta_file_path = '/tmp/test.fasta'
    with open(fasta_file_path, 'w') as f:
        f.write(fasta_content)
    yield fasta_file_path
    os.remove(fasta_file_path)

@pytest.fixture
def empty_file():
    empty_file_path = '/tmp/empty.fasta'
    with open(empty_file_path, 'w') as f:
        f.write('')
    yield empty_file_path
    os.remove(empty_file_path)

@pytest.fixture
def no_seq_file():
    no_seq_content = ">seq1\n>seq2\n>seq3"
    no_seq_file_path = '/tmp/no_seq.fasta'
    with open(no_seq_file_path, 'w') as f:
        f.write(no_seq_content)
    yield no_seq_file_path
    os.remove(no_seq_file_path)

def test_read_fasta(fasta_file):
    expected_output = {
        'seq1': 'ATGCGTA',
        'seq2': 'CGTACGTAGCTA',
        'seq3': 'GCTAGCTAGCTA'
    }
    result = read_fasta(fasta_file)
    assert result == expected_output

def test_read_fasta_empty_file(empty_file):
    result = read_fasta(empty_file)
    assert result == {}

def test_read_fasta_no_sequences(no_seq_file):
    expected_output = {'seq1': '', 'seq2': '', 'seq3': ''}
    result = read_fasta(no_seq_file)
    assert result == expected_output

def test_read_first_fasta(fasta_file):
    expected_output = 'ATGCGTA'
    result = read_first_fasta(fasta_file)
    assert result == expected_output

def test_read_first_fasta_empty_file(empty_file):
    result = read_first_fasta(empty_file)
    assert result == ''

def test_read_first_fasta_no_sequences(no_seq_file):
    result = read_first_fasta(no_seq_file)
    assert result == ''


def test_complement():
    assert complement('ATCG') == 'TAGC'
    assert complement('atcg') == 'tagc'
    assert complement('AATTCCGG') == 'TTAAGGCC'
    assert complement('aattccgg') == 'ttaaggcc'
    assert complement('ATCGU') == 'TAGCA'
    assert complement('atcgu') == 'tagca'

def test_complement_invalid_sequence():
    with pytest.raises(ValueError):
        complement('ATXG')
    with pytest.raises(ValueError):
        complement('1234')
    with pytest.raises(ValueError):
        complement('ATCGX')


