import numpy as np
import copy
from Bio.Seq import Seq

ALPHABET = {'N': 'N', 'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}

class SeqMat:
    ROW_SEQ = 0
    ROW_INDS = 1
    ROW_SUPERINDS = 2
    ROW_MUTATED = 3

    def __init__(self, seqmat, alphabet=None):
        self.seqmat = seqmat
        self.alphabet = alphabet or {'N': 'N', 'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
        self.char_to_value = {c: i for i, c in enumerate(self.alphabet.keys())}
        self.value_to_char = {i: c for i, c in enumerate(self.alphabet.keys())}
        self.value_complements = {self.char_to_value[c1]: self.char_to_value[c2] for c1, c2 in self.alphabet.items()}

    def __repr__(self):
        return f"<SeqMat: {self.seq}>"

    def __str__(self):
        return self.seq

    def __len__(self):
        return self.seqmat.shape[1]

    def __getitem__(self, key):
        if isinstance(key, slice):
            pos1, pos2 = self._rel_index(key.start), self._rel_index(key.stop)
            return SeqMat(self.seqmat[:, pos1:pos2])
        else:
            pos = self._rel_index(key)
            return SeqMat(self.seqmat[:, pos:pos + 1])

    def __contains__(self, other):
        """
        Checks if another SeqMat object is entirely contained within this SeqMat object.

        Args:
            other (SeqMat): Another SeqMat object to check for containment.

        Returns:
            bool: True if `other` is contained in `self`, False otherwise.
        """
        # Ensure `other` is a SeqMat
        if not isinstance(other, SeqMat):
            raise TypeError("Can only check containment with another SeqMat object.")

        # Check if all indices of `other` are in `self`
        other_indices = other.seqmat[other.ROW_INDS, :]
        self_indices = self.seqmat[self.ROW_INDS, :]
        if not np.all(np.isin(other_indices, self_indices)):
            return False

        return True

    def __eq__(self, other):
        """
        Implements the == operator to compare two SeqMat objects.

        Args:
            other (SeqMat): The other SeqMat object to compare.

        Returns:
            bool: True if the two SeqMat objects are equal, False otherwise.
        """
        # Ensure `other` is a SeqMat object
        if not isinstance(other, SeqMat):
            return False

        # Compare the sequence matrix
        if not np.array_equal(self.seqmat, other.seqmat):
            return False

        return True

    @classmethod
    def empty(cls, alphabet=None):
        """
        Creates an empty SeqMat object.

        Args:
            alphabet (dict): Optional alphabet dictionary (default: {'N': 'N', 'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}).

        Returns:
            SeqMat: An empty SeqMat object.
        """
        empty_seqmat = np.zeros((4, 0), dtype=np.int32)  # 4 rows, 0 columns (no data)
        return cls(empty_seqmat, alphabet=alphabet)

    def __add__(self, other):
        """
        Implements the + operator. Joins two SeqMat objects or applies mutations.

        If `other` is outside the range of indices, the sequences are concatenated, provided the indices are
        monotonically increasing or decreasing. Otherwise, it applies the mutation.

        Args:
            other (SeqMat): Another SeqMat object to join or mutate.

        Returns:
            SeqMat: A new SeqMat object with the resulting sequence.
        """
        # Ensure `other` is a SeqMat
        if not isinstance(other, SeqMat):
            raise TypeError("Can only add another SeqMat object.")

        if other in self:
            return self.mutate(other)

        else:
            combined_seqmat = np.hstack((self.seqmat, other.seqmat))

        # Ensure the combined sequence is monotonic
        if not self._is_monotonic(combined_seqmat[self.ROW_INDS]):
            raise ValueError("Resulting sequence indices are not monotonic.")

        return SeqMat(combined_seqmat, alphabet=self.alphabet)

    def __iadd__(self, other):
        """
        Implements the += operator. Joins two SeqMat objects or applies mutations in place.

        Args:
            other (SeqMat): Another SeqMat object to join or mutate.

        Returns:
            SeqMat: The mutated or joined SeqMat object.
        """
        # Ensure `other` is a SeqMat
        if not isinstance(other, SeqMat):
            raise TypeError("Can only add another SeqMat object.")

        if other in self:
            self.seqmat = self.mutate(other).seqmat
            return self
        else:
            self.seqmat = np.hstack((self.seqmat, other.seqmat))

        if not self._is_monotonic(self.seqmat[self.ROW_INDS]):
            raise ValueError("Resulting sequence indices are not monotonic.")

        return self

    def get_context(self, pos, context=500):
        pos = self._rel_index(pos)
        lower_bound, upper_bound = max(0, pos - context), min(len(self), pos + context + 1)
        return SeqMat(self.seqmat[:, lower_bound:upper_bound])

    def _rel_index(self, pos):
        if pos in self.indices:
            return np.where(self.seqmat[self.ROW_INDS, :] == pos)[0][0]
        else:
            raise IndexError(f"Position {pos} not found in sequence.")

    def _is_same_strand(self, other):
        """
        Checks if two SeqMat objects are on the same strand.

        Args:
            other (SeqMat): The other SeqMat object to compare.

        Returns:
            bool: True if both are on the same strand, False otherwise.
        """
        self_indices = self.seqmat[self.ROW_INDS, :]
        other_indices = other.seqmat[self.ROW_INDS, :]

        # Determine monotonicity
        self_increasing = np.all(np.diff(self_indices) >= 0)
        self_decreasing = np.all(np.diff(self_indices) <= 0)
        other_increasing = np.all(np.diff(other_indices) >= 0)
        other_decreasing = np.all(np.diff(other_indices) <= 0)

        # Both must be either increasing or decreasing
        return (self_increasing and other_increasing) or (self_decreasing and other_decreasing)

    def reverse_complement(self, inplace=True):
        """
        Reverse complement the sequence in place.
        """
        seqmat = self.seqmat[:, ::-1].copy()
        seqmat[self.ROW_SEQ, :] = np.vectorize(self.value_complements.get)(seqmat[self.ROW_SEQ])

        if inplace:
            self.seqmat = seqmat
            return self

        return SeqMat(seqmat)

    @classmethod
    def from_seq(cls, seq_dict, alphabet=None):
        """
        Create a SeqMat object from a dictionary containing sequence information.
        """
        seq = np.array(list(seq_dict["seq"]))
        inds = seq_dict.get("indices", np.arange(len(seq), dtype=np.int32))
        superinds = seq_dict.get("superinds", np.zeros(len(seq), dtype=np.int32))
        mutmark = np.zeros_like(superinds)

        assert len(seq) == len(inds), f"Sequence length {len(seq)} must match indices length {len(inds)}"
        if not cls._is_monotonic(inds):
            raise ValueError(f"Sequence indices must be monotonic, got {inds}")

        # Create character-to-value mapping
        char_to_value = {c: i for i, c in enumerate(ALPHABET.keys())}
        seq_values = [char_to_value[nt] for nt in seq]

        # Stack sequence matrix
        seqmat = np.vstack([seq_values, inds, superinds, mutmark]).astype(np.int32)
        return cls(seqmat)

    @staticmethod
    def _is_monotonic(inds):
        return all(x >= y for x, y in zip(inds, inds[1:])) if inds[0] > inds[-1] else all(
            x <= y for x, y in zip(inds, inds[1:]))

    @property
    def seq(self):
        return self.rawseq.replace('-', '')

    @property
    def rawseq(self):
        return ''.join([self.value_to_char[int(ind)] for ind in self.seqmat[self.ROW_SEQ, :]])

    @property
    def indices(self):
        return self.seqmat[self.ROW_INDS, self.seqmat[self.ROW_SEQ, :] != 0] + (
                    self.seqmat[self.ROW_SUPERINDS, self.seqmat[self.ROW_SEQ, :] != 0] / 10)

    def mutate(self, mut):
        """
        Apply mutations to the sequence matrix.
        Args:
            mut (SeqMat): A SeqMat object containing mutations.
            return_seqmat (bool): If True, return the mutated seqmat; otherwise, return updated sequence.

        Returns:
            str or np.ndarray: Mutated sequence or sequence matrix based on `return_seqmat`.
        """
        # Ensure strand compatibility
        if not self._is_same_strand(mut):
            raise ValueError("Mutation and sequence are not on the same strand.")

        # something to make sure the mutation is contained as one deletion, insertion, or snp or indel
        ref_seqmat = self.seqmat.copy()
        mut_seqmat = mut.seqmat

        # Ensure mutation indices exist in the reference
        if not np.all(np.isin(mut_seqmat[self.ROW_INDS, :], ref_seqmat[self.ROW_INDS, :])):
            return self

        # Handle the fact that only part of the mutation is in the sequence and isertable
        if not np.all(np.isin(mut_seqmat[self.ROW_INDS, :], ref_seqmat[self.ROW_INDS, :])):
            raise ValueError("Some mutation indices are not found in the reference sequence.")

        # Handle insertions
        insertions = np.where(mut_seqmat[self.ROW_SUPERINDS, :] > 0)[0]
        if insertions.size > 0:
            ins_seqmat = mut_seqmat[:, insertions]
            ins_loc = np.where(ref_seqmat[self.ROW_INDS, :] == ins_seqmat[self.ROW_INDS, 0])[0][0] + 1
            ref_seqmat = np.insert(ref_seqmat, ins_loc, ins_seqmat.T, axis=1)

        # Handle replacements
        np.where(mut_seqmat[self.ROW_SUPERINDS, :] == 0)[0]
        condition = (
            np.isin(ref_seqmat[self.ROW_INDS, :],
                    mut_seqmat[self.ROW_INDS, np.where(mut_seqmat[self.ROW_SUPERINDS, :] == 0)[0]])
        )

        indices = np.where(condition)[0]
        ref_seqmat[:, indices] = mut_seqmat[:, :]

        return SeqMat(ref_seqmat)

    def orf_seqmat(self, tis_index):
        temp = SeqMat(self.seqmat[:, tis_index:])  # .drop_indices()
        raw_seq = temp.seq  # Extract the raw sequence
        pattern = re.compile(r"(?:[NACGT]{3})*?(TAA|TAG|TGA)")
        match = pattern.match(raw_seq)
        if match:
            stop_index = match.end()
        else:
            stop_index = len(raw_seq)
        end_index = tis_index + stop_index // 3

    def translate(self, tis_index):
        from Bio.Seq import Seq
        return Seq(self.orf_seqmat(tis_index).seq).translate()


class MutSeqMat(SeqMat):
    """
    A subclass of SeqMat designed specifically for mutation sequences.

    Additional Conditions:
    1. Mutation indices must be consecutive (increasing or decreasing).
    2. The superinds row must have a maximum value of 10.
    """

    def __init__(self, seqmat, alphabet=None):
        super().__init__(seqmat, alphabet)

        # Validate the mutation-specific conditions
        self._validate_mutation_indices()
        self.seqmat[-1, :] = 1
        # self._validate_superinds()

    def _validate_mutation_indices(self):
        """
        Validates that the mutation indices are consecutive (increasing or decreasing).
        """
        indices = self.seqmat[self.ROW_INDS, :]
        if not (np.all(abs(np.diff(indices)) <= 1)):
            raise ValueError(f"Mutation indices must be consecutive. Got: {indices}")

    # def _validate_superinds(self):
    #     """
    #     Validates that the superinds row has a maximum value of 10.
    #     """
    #     superinds = self.seqmat[self.ROW_SUPERINDS, :]
    #     if np.max(superinds) > 10:
    #         raise ValueError(f"Superinds row must have a maximum value of 10. Got: {superinds}")

