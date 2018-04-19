"""A Module for Assignment  1, calculating the merkle root of the data

    Classes:
        MerkleBuilder -- for calculating the Merkle Tree Root from a file
"""
from hashlib import sha256
from typing import List


class MerkleBuilder:
    """A class for calculating the Merkle Tree Root from a file
    
    Arguments:
        filename {str} -- The name of the file containing the data to hash
        duplicate_odds {bool} -- Should the last node in an odd number length
            input be duplicated. (default: False)
    """

    def __init__(self, filename: str, duplicate_odds: bool = False):
        self.filename = filename
        self.duplicate_odds = duplicate_odds

    def build_tree(self) -> str:
        """Calculates the hash of the Merkle Tree root
        
        Returns:
            str -- The Merkle Tree root as a string of hex digits
        """
        # Read in data from file
        data = self._load_data()

        # Do first encoding
        hashes = self._calculate_first_hash(data)

        # Performs next step of hashing tree
        return self._recursive_hash(hashes)

    def _load_data(self) -> List[str]:
        """Reads the file lines into a list with spaces and newlines removed"""
        with open(self.filename) as file:
            return [l for l in (line.strip() for line in file.readlines()) if l]

    def _calculate_first_hash(self, data: List[str]) -> List[str]:
        """Maps the sha256 algorithm over the items provided
        
        Arguments:
            data {List[str]} -- The data to map over
        
        Returns:
            List[str] -- A list of the data's hashes as hex digits
        """
        return [sha256(d.encode()).hexdigest() for d in data]

    def _recursive_hash(self, hashes: List[str]) -> List[str]:
        """
        Recursively hash pairs of hashes from the input list to build up
        each layer of the tree.
        """
        # Base case is just two input
        if len(hashes) == 2:
            return self._hash_two(hashes[0], hashes[1])

        # If odd, duplicate as necessary
        if len(hashes) % 2 == 1:
            if self.duplicate_odds:
                hashes.append(hashes[len(hashes) - 1])
            else:
                hashes.append('')

        # Recursive, keep hashing pairs
        next_hashes = [self._hash_two(hashes[i], hashes[i + 1]) 
                       for i 
                       in range(0, len(hashes), 2)]
                       
        return self._recursive_hash(next_hashes)

    @staticmethod
    def _hash_two(hash_1: str, hash_2: str):
        """Takes two hashes and hashes them as one concatenated input"""
        return sha256(hash_1.encode() + hash_2.encode()).hexdigest()


def main():
    print('Calculating even Merkle root:')
    mb_e = MerkleBuilder('even_transactions.txt')
    e_result = mb_e.build_tree()
    print(f'\tThe root is: {e_result}')

    print('Calculating odd Merkle root without duplication:')
    mb_o = MerkleBuilder('odd_transactions.txt')
    o_result = mb_o.build_tree()
    print(f'\tThe root is: {o_result}')

    print('Calculating odd Merkle root with duplication:')
    mb_o_dup = MerkleBuilder('odd_transactions.txt', duplicate_odds=True)
    o_dup_result = mb_o_dup.build_tree()
    print(f'\tThe root is: {o_dup_result}')


if __name__ == "__main__":
    main()