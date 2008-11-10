#!/usr/bin/env python2.4
import parse_puzzle_pack
import unittest

class TestCheckPuzzlePack(unittest.TestCase):
  def testEmptyCase(self):
    self.assertEqual([], parse_puzzle_pack.ParseString(''))

  def testOnOneGoodPuzzle(self):
    file_string = '''
    
    1
    Z is E.
    I'm feeling puzzled. 
    J'n gzzmjoh qvaamze.
    
    '''
    [puzzle] = parse_puzzle_pack.ParseString(file_string)
    self.assertEqual('1', puzzle['name'])
    self.assertEqual('Z is E.', puzzle['short_clue'])
    self.assertEqual('I\'m feeling puzzled.', puzzle['solution_text'])
    self.assertEqual('J\'n gzzmjoh qvaamze.', puzzle['cipher_text'])

  def testOnTwoGoodPuzzles(self):
    file_string = '''
    
    1
    Z is E.
    I'm feeling puzzled. 
    J'n gzzmjoh qvaamze.
        
    2
    H is G
    Go team!
    Hp sfbn!

    '''
    [puzzle1, puzzle2] = parse_puzzle_pack.ParseString(file_string)
    expected1 = {'name': '1',
                 'short_clue': 'Z is E.',
                 'solution_text': 'I\'m feeling puzzled.',
                 'cipher_text': 'J\'n gzzmjoh qvaamze.'}
    expected2 = {'name': '2',
                 'short_clue': 'H is G.',
                 'solution_text': 'Go team!',
                 'cipher_text': 'Hp sfbn!'}
    self.assertEqual(expected1, puzzle1)
    self.assertEqual(expected2, puzzle2)
  
  def testWhereOnePuzzleHasAnError(self):
    file_string = '''
    
    2
    H is G
    Go team!
    Hp sfbn!

    1
    Z is E.
    I'm feeling puzzled. 
    J'n gyzmjoh qvaamfe.
        
    '''
    try:
      parse_puzzle_pack.ParseString(file_string)
      self.fail('Expected a value error on incorrect puzzle.')
    except ValueError, e:
      self.assertTrue('puzzle 1' in str(e).lower())

if __name__ == '__main__':
  unittest.main()