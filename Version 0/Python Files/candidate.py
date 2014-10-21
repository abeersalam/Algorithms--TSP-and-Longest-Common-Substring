#
# candidate.py
# combinatorial candidate generation
# CSUF CPSC 335 - Spring 2014
#
# In case it matters, this file is licensed according to the BSD
# 2-clause license:
#
# Copyright (c) 2014, Kevin Wortman
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 
#     Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
# 
#     Redistributions in binary form must reproduce the above
#     copyright notice, this list of conditions and the following
#     disclaimer in the documentation and/or other materials provided
#     with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import unittest

# Returns a list of all subsets of the given list L, in an unspecified
# order.
def eager_subsets(L):
    result = [ [] ]
    for x in L:
        with_x = [ subset + [x] for subset in result ]
        result = result + with_x
    return result

# Returns a list of all permutations of the given list L, in an
# unspecified order.
def eager_permutations(L):
    result = [ [] ]
    for x in L:
        extended = []
        for S in result:
            for k in range(len(S)+1):
                extended.append(S[:k] + [x] + S[k:])

        result = extended
    return result

# Base class for all candidate generator factory classes. The has_next
# and next member functions should be redefined by subclasses.
class CandidateFactory:
    def has_next(self):
        raise NotImplementedError

    def next(self):
        raise NotImplementedError

# Lazily generates subsets of the list L. Usage example:
#
#   factory = SubsetFactory(L)
#   while factory.has_next():
#     subset = factory.next()
#     <do something with subset>
class SubsetFactory:
  def __init__(self, L):
    self.L = L
    self.n = len(L)
    self.i = 0  # will iterate from 0 to 2^n-1

  # return True if and only if the factory can generate another candidate
  def has_next(self):
    return self.i < (2 ** self.n) # i < 2^n

  # return the next candidate
  def next(self):
    # generate subset S
    S = []
    for k in range(self.n):
      # S[k] is in this subset iff bit k of self.i is 1
      if ((self.i >> k) & 1) == 1:
        S.append(self.L[k])

    # advance to next subset
    self.i += 1

    # return this subset
    return S
    
# Lazily generates permutations of the list L.
class PermutationFactory(CandidateFactory):
    # This implements the Steinhaus-Johnson-Trotter algorithm.
    def __init__(self, L):
        # Each permutation element has a rank (which is its index in
        # L), the value L[rank] itself, and a speed to track its
        # direction in the S-J-T algorithm.
        self.elts = [ PermutationElt(rank=i, value=L[i])
                      for i in range(len(L)) ]

        # Keep track of whether the last permutation has been returned
        # yet.
        self.has_next_flag = True

    # Returns the valid index that elt[index] would like to move to
    # according to its direction, or None if it is pointing off the
    # end of the permutation.
    def _focus(self, index):
        f = index + self.elts[index].speed
        if 0 <= f and f < len(self.elts):
            return f
        else:
            return None

    # Returns the index of the highest-ranked mobile element, or None
    # if there are no mobile elements left.
    def _find_mobile(self):
        m = None
        for i in range(len(self.elts)):
            f = self._focus(i)
            if f is not None and self.elts[i].rank > self.elts[f].rank:
                if m is None or self.elts[i].rank > self.elts[m].rank:
                    m = i
        return m
        
    def has_next(self):
        return self.has_next_flag

    def next(self):
        # First generate the list to return from our internal
        # PermutationElt list.
        result = [ elt.value for elt in self.elts ]

        # Find which element to move.
        m = self._find_mobile()
        if m is None:
            # If no elements can be moved anymore, this is the last
            # permutation.
            self.has_next_flag = False
        else:
            # Extract the rank and focus index of the element we will
            # move. (The next step will scramble indices around so it
            # is convenient to pull these values out now.)
            rank = self.elts[m].rank
            f = self._focus(m)

            # Swap the elements at indices m and f.
            self.elts[m], self.elts[f] = self.elts[f], self.elts[m]
                
            # Reverse the direction of any elements ranked higher than
            # the one we just moved.
            for elt in self.elts:
                if elt.rank > rank:
                    elt.reverse()

        return result

# Helper class for the PermutationFactory class.
class PermutationElt:
    def __init__(self, rank, value):
        self.rank = rank
        self.value = value
        self.speed = -1

    def reverse(self):
        self.speed *= -1

# unit tests
class TestCandidateGenerators(unittest.TestCase):
    def assertEqualUnordered(self, a, b):
        self.assertEqual(sorted(a), sorted(b))

    def test_eager_subsets(self):
        self.assertEqual(sorted(eager_subsets([])),
                         sorted([ [] ]))
        self.assertEqual(sorted(eager_subsets([1])),
                         sorted([ [], [1] ]))
        self.assertEqual(sorted(eager_subsets([1, 2])),
                         sorted([ [], [1], [2], [1, 2] ]))
        self.assertEqual(sorted(eager_subsets([1, 2, 3])),
                         sorted([ [], 
                                  [1], [2], [3],
                                  [1, 2], [1, 3], [2, 3],
                                  [1, 2, 3] ]))

    def test_eager_permutations(self):
        self.assertEqual(sorted(eager_permutations([1])), 
                         sorted([ [1] ]))
        self.assertEqual(sorted(eager_permutations([1, 2])),
                         sorted([ [1, 2], [2, 1] ]))
        self.assertEqual(sorted(eager_permutations([1, 2, 3])),
                         sorted([ [1, 2, 3],
                                  [1, 3, 2],
                                  [2, 1, 3],
                                  [2, 3, 1],
                                  [3, 1, 2],
                                  [3, 2, 1] ]))

    def factory_to_list(self, factory):
        result = []
        while factory.has_next():
            result.append(factory.next())
        return result

    def test_SubsetFactory(self):
        for n in range(9):
            L = list(range(n))
            self.assertEqualUnordered(eager_subsets(L),
                                      self.factory_to_list(SubsetFactory(L)))

    def test_PermutationFactory(self):
        self.factory_to_list(PermutationFactory(list(range(3))))

        self.assertEqualUnordered(self.factory_to_list(PermutationFactory([1])),
                                  [ [1] ])
        self.assertEqualUnordered(self.factory_to_list(PermutationFactory([1, 2])),
                                  [ [1, 2], [2, 1] ])
        self.assertEqualUnordered(self.factory_to_list(PermutationFactory([1, 2, 3])),
                                  [ [1, 2, 3],
                                    [1, 3, 2],
                                    [2, 1, 3],
                                    [2, 3, 1],
                                    [3, 1, 2],
                                    [3, 2, 1] ])

        for n in range(1, 9):
            L = list(range(n))
            self.assertEqualUnordered(eager_permutations(L),
                                      self.factory_to_list(PermutationFactory(L)))

if __name__ == '__main__':
    unittest.main()
