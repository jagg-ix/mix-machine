# test_memory.py

# module for testing class Memory and functions mix2dec, dec2mix

import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'assembler'))
from parse_line import *
from memory import *

class MemoryTestCase(unittest.TestCase):
  def checkWords(self, word1, word2):
    if word1[1:] != [0, 0, 0, 0, 0]:
      self.assertEqual(word1,word2)
    else:
      self.assertEqual([0, 0, 0, 0, 0], word2[1:])

  def testConvert(self):
    tests = [ # pairs (mix_word, decimal)
      ([+1,  0,  0,  0,  0,  1], 1),
      ([+1,  0,  0,  1,  0,  0], 4096),
      ([-1,  0,  0,  1,  0,  0], -4096),
      ([-1,  1,  2,  3,  4,  5], -17314053),
      ([+1, 63, 62, 61, 60,  0], 1073471232),
      ([+1,  0,  0,  0,  0,  0], 0),
      ([-1,  0,  0,  0,  0,  0], 0),
      ([-1,  0,  0,  0,  0,  0], -0),
      ([+1,  0,  0,  0,  0,  0], -0)
    ]
    for word, dec in tests:
      self.assertEqual(Memory.mix2dec(word), dec)
      self.checkWords(Memory.dec2mix(dec), word)


  def test_apply_to_word(self):
    def colon(l, r):
      return 8*l + r

    word = [+1, 1, 2, 3, 4, 5]

    self.assertTrue(Memory.apply_to_word(0, word, colon(2, 3)) is not None)
    self.assertEqual(word, [+1, 1, 0, 0, 4, 5])

    self.assertTrue(Memory.apply_to_word(153121157, word, colon(1, 4)) is not None)
    self.assertEqual(word, [+1, 8, 7, 6, 5, 5])

    self.assertTrue(Memory.apply_to_word(-433, word, colon(0, 0)) is not None)
    self.assertEqual(word, [-1, 8, 7, 6, 5, 5])

    self.assertTrue(Memory.apply_to_word(0, word, colon(-1, -1)) is None)
    self.assertTrue(Memory.apply_to_word(0, word, colon(-1, 0)) is None)
    self.assertTrue(Memory.apply_to_word(0, word, colon(6, 0)) is None)
    self.assertTrue(Memory.apply_to_word(0, word, colon(0, -1)) is None)
    self.assertTrue(Memory.apply_to_word(0, word, colon(3, 2)) is None)

  def testMemory_set_word(self):
    memory = Memory()
    value_tests = [ # (word_index, value, word)
      (0, 1073471232, [+1, 63, 62, 61, 60, 00]),
      (3999, -113, [-1, 0, 0, 0, 1, 49]),
      (3999, +113, [+1, 0, 0, 0, 1, 49]),
    ]
    for word_index, value, word in value_tests:
      memory[word_index] = value
      self.assertEqual(memory.memory[word_index], word)

  def testMemory_cmp_memory(self):
    memory = Memory()
    test = ( # pairs (value, addr)
      (1,           0),
      (4096,        33),
      (-4096,       77),
      (-17314053,   999),
      (1073471232,  2000),
      (0,           3998),
      (64,          3999)
    )
    memory_part = {
      0:    [+1,  0,  0,  0,  0,  1],
      1:    [+1,  0,  0,  0,  0,  0],
      33:   [+1,  0,  0,  1,  0,  0],
      77:   [-1,  0,  0,  1,  0,  0],
      999:  [-1,  1,  2,  3,  4,  5],
      2000: [+1, 63, 62, 61, 60,  0],
      3998: [+1,  0,  0,  0,  0,  0],
      3999: [+1,  0,  0,  0,  1,  0]
    }
    for value, addr in test:
      memory[addr] = value

    self.assertEqual(memory, memory_part)

    memory = Memory()
    test = ( # pairs (value, addr)
      (1,           0),
      (4096,        33),
      (-4096,       77),
      (-17314053,   999),
      (1073471232,  2000),
      (0,           3998),
      (64,          3999)
    )
    memory_part_1 = { # odd word#1
      0:    [+1,  0,  0,  0,  0,  1],
      1:    [+1,  0, 11, 11, 11, 11],
      33:   [+1,  0,  0,  1,  0,  0],
      77:   [-1,  0,  0,  1,  0,  0],
      999:  [-1,  1,  2,  3,  4,  5],
      2000: [+1, 63, 62, 61, 60,  0],
      3998: [+1,  0,  0,  0,  0,  0],
      3999: [+1,  0,  0,  0,  1,  0]
    }
    memory_part_2 = { # no word#33
      0:    [+1,  0,  0,  0,  0,  1],
      77:   [-1,  0,  0,  1,  0,  0],
      999:  [-1,  1,  2,  3,  4,  5],
      2000: [+1, 63, 62, 61, 60,  0],
      3998: [+1,  0,  0,  0,  0,  0],
      3999: [+1,  0,  0,  0,  1,  0]
    }
    for value, addr in test:
      memory[addr] = value

    self.assertNotEqual(memory, memory_part_1)
    self.assertNotEqual(memory, memory_part_2)

  def test_positive_zero(self):
    self.assertEqual(Memory.positive_zero(), [+1, 0, 0, 0, 0, 0])

  def test_validness(self):
    for adr in (0,1,333,3999):
      self.assertTrue(Memory().is_valid_address(adr))
    
    for adr in (-1,4000,4001):
      self.assertFalse(Memory().is_valid_address(adr))

suite = unittest.makeSuite(MemoryTestCase, 'test')

if __name__ == "__main__":
	unittest.main()
