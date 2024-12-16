'''
Author: Chou_Uken Chouuken@outlook.com
Date: 2024-12-13 14:29:16
LastEditors: Chou_Uken Chouuken@outlook.com
LastEditTime: 2024-12-14 18:17:36
FilePath: /seqfkit/seqfkit/utils.py
'''

def read_fasta(file_path: str) -> dict[str, str]:
    """Reads a FASTA file and returns a dictionary with sequence IDs as keys and sequences as values.

    Args:
        file_path (str): Path to the FASTA file
    Returns:
        Dict[str, str]: Dictionary with sequence IDs as keys and sequences as values
    """

    sequences: dict[str, str] = {}
    with open(file=file_path, mode='r', encoding='utf-8') as file:
        line: str = file.readline()
        this_id: str = ''
        this_seq: str = ''
        if (line.startswith('>')):
            this_id = line.lstrip('>').strip()
        while (line):
            line = file.readline()
            if (line):
                # More contents to be read...
                if (line.startswith('>')):
                    # New sequence!
                    if (this_id):
                        sequences[this_id] = this_seq
                        this_id = line.lstrip('>').strip()
                        this_seq = ''
                    else:
                        this_id = line.lstrip('>').strip()
                else:
                    if (this_id):
                        # Append last sequence...
                        this_seq += line.strip()
                    else:
                        # Lipsum...
                        pass
            else:
                # No more...
                if (this_id):
                    sequences[this_id] = this_seq
                    break

    return (sequences)


def read_first_fasta(file_path: str) -> str:
    """Reads the first sequence from a FASTA file and returns it as a string.

    Args:
        file_path (str): Path to the FASTA file
    Returns:
        str: The first sequence in the FASTA file
    """
    with open(file=file_path, mode='r', encoding='utf-8') as file:
        line: str = file.readline()
        this_seq: str = ''
        while (line):
            if (line.startswith('>')):
                if (this_seq):
                    break
            else:
                this_seq += line.strip()
            line = file.readline()
    return (this_seq)


def complement(seq: str) -> str:
    """Generates the complementary DNA sequence.

    Args:
        seq (str): Original DNA sequence
    Returns:
        str: Complementary DNA sequence
    """

    if not all(c in 'ATCGUatcgu' for c in seq):
        # DNA序列验证
        raise ValueError("Invalid DNA sequence: only A(a), T(t), C(c), G(g), U(u) are allowed.")

    complement_map = str.maketrans('ATCGUatcgu', 'TAGCAtagca')
    return (seq.translate(complement_map))


