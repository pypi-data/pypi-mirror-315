"""
This file combines the two frameworks doctest and unittest to test various aspects of the
BIDSBehEvent class.
"""

import doctest
import unittest

from psychopy_bids import bids


class TestBIDSBehEvent(unittest.TestCase):
    """Providing unit tests for the class BIDSBehEvent"""

    def test_init(self):
        """Test case for the __init__ method of BIDSBehEvent"""
        event = bids.BIDSBehEvent(some_attribute=42, another_attribute="abc")
        self.assertEqual(event.some_attribute, 42)
        self.assertEqual(event.another_attribute, "abc")

    # -------------------------------------------------------------------------------------------- #

    def test_repr(self):
        """Test case for the __repr__ method of BIDSBehEvent"""
        event = bids.BIDSBehEvent(some_attribute=42, another_attribute="abc")
        expected_repr = "BIDSBehEvent(some_attribute=42, another_attribute=abc)"
        self.assertEqual(repr(event), expected_repr)

    # -------------------------------------------------------------------------------------------- #

    def test_doc_strings(self):
        """Test docstrings using doctest and pytest."""
        results = doctest.testmod(bids.bidsbehevent)
        self.assertEqual(
            results.failed,
            0,
            f"{results.failed} doctests failed out of {results.attempted}.",
        )


# ------------------------------------------------------------------------------------------------ #


if __name__ == "__main__":
    unittest.main()
