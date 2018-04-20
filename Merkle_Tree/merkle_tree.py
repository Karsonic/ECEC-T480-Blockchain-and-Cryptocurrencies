"""A Module for Assignment  1, calculating the merkle root of the data

    Classes:
        MerkleNode -- Node of a Merkle Tree
        MerkleBuilder -- For calculating the Merkle Tree root from a file
"""
from hashlib import sha256
from typing import List


class MerkleNode:
    """A node of a Merkle Tree

     Attributes:
        hash {str} -- The hash value of the node (default: {''})
        p_node {MerkleNode} -- the parent node (default: {None})
        l_node {MerkleNode} -- the left child node (default: {None})
        r_node {MerkleNode} -- the right child node (default: {None})
    """

    def __init__(self, hash: str = '', p_node: 'MerkleNode' = None, 
                 l_node: 'MerkleNode' = None, r_node: 'MerkleNode' = None):
        self.hash = hash
        self.p_node = p_node
        self.l_node = l_node
        self.r_node = r_node

    def __str__(self, level=0):
        ret = '{0} {1}\n'.format("\t"*level, repr(self.hash))
        if self.l_node is not None:
            ret += self.l_node.__str__(level + 1)
        if self.r_node is not None:
            ret += self.r_node.__str__(level + 1)
        return ret

    def __repr__(self):
        return '<Merkle tree node representation>'

    @staticmethod
    def make_parent(node_l: 'MerkleNode', node_r: 'MerkleNode') -> 'MerkleNode':
        """Takes two nodes and hashes them to make their parent node.

        Note: This also sets the provided nodes as the new node's children

        Attributes: 
            node_l {MerkleNode} -- The node to be the left child
            node_r {MerkleNode} -- The node to be the right child
        
        Returns:
            MerkleNode -- The newly created parent node
        """
        hash = sha256(node_l.hash.encode() + node_r.hash.encode()).hexdigest()
        return MerkleNode(hash, None, node_l, node_r)


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

    def build_tree(self) -> MerkleNode:
        """Calculates the Merkle Tree root
        
        Returns:
            MerkleNode -- The Merkle Tree root
        """
        # Read in data from file
        data = self._load_data()
        # Do first encoding
        nodes = self._calculate_first_nodes(data)
        # Performs next step of hashing tree
        return self._recursive_hash(nodes)[0]

    def _load_data(self) -> List[str]:
        """Reads the file lines into a list with spaces and newlines removed"""
        # This also removes blank lines
        with open(self.filename) as file:
            return [l for l in (line.strip() for line in file.readlines()) if l]

    def _calculate_first_nodes(self, data: List[str]) -> List[MerkleNode]:
        """Makes orphan MerkleNodes out of the sha256 hashes of the input list
        
        Arguments:
            data {List[str]} -- The data to map over
        
        Returns:
            List[MerkleNode] -- The resulting MerkleNodes
        """
        return [MerkleNode(sha256(d.encode()).hexdigest()) for d in data]

    def _recursive_hash(self, nodes: List[MerkleNode]) -> List[MerkleNode]:
        """
        Recursively hash pairs of nodes from the input list to build up
        each layer of the tree.
        """
        # Base case is just two input
        if len(nodes) == 2:
            return [MerkleNode.make_parent(nodes[0], nodes[1])]

        # If odd, duplicate as necessary
        if len(nodes) % 2 == 1:
            if self.duplicate_odds:
                nodes.append(nodes[len(nodes) - 1])
            else:
                nodes.append(MerkleNode())

        # Recursive, keep hashing pairs
        next_nodes = [MerkleNode.make_parent(nodes[i], nodes[i + 1]) 
                       for i 
                       in range(0, len(nodes), 2)]

        # Set the parents and children           
        for i, node in enumerate(nodes):
            node.parent = next_nodes[i//2]

        return self._recursive_hash(next_nodes)


def main():
    print('Calculating even Merkle root:')
    mb_e = MerkleBuilder('even_transactions.txt')
    e_result = mb_e.build_tree()
    print(f'\tThe root is: {e_result.hash}')
    print(f'\tThe full tree is:\n {e_result}')

    print('Calculating odd Merkle root without duplication:')
    mb_o = MerkleBuilder('odd_transactions.txt')
    o_result = mb_o.build_tree()
    print(f'\tThe root is: {o_result.hash}')
    print(f'\tThe full tree is:\n {o_result}')

    print('Calculating odd Merkle root with duplication:')
    mb_o_dup = MerkleBuilder('odd_transactions.txt', duplicate_odds=True)
    o_dup_result = mb_o_dup.build_tree()
    print(f'\tThe root is: {o_dup_result.hash}')
    print(f'\tThe full tree is:\n {o_dup_result}')


if __name__ == "__main__":
    main()
