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
    # This is a comment.
    
    1
    Z is E.
    I'm feeling puzzled. 
    J'n gzzmjoh qvaamze.

    # Here's another comment.
        
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

  def testConvertPuzzleToCsvLine_EmptyCase(self):
    puzzle = {'name': '',
              'short_clue': '',
              'solution_text': '',
              'cipher_text': ''}
    csv = parse_puzzle_pack.ConvertPuzzleToCsvLine(puzzle=puzzle,
                                                   pack_title='')
    expected = ',,,,'
    self.assertEqual(expected, csv)

  def testConvertPuzzleToCsvLine(self):
    puzzle = {'name': 'Name',
              'short_clue': 'Clue',
              'solution_text': 'Soln',
              'cipher_text': 'Cipher'}
    csv = parse_puzzle_pack.ConvertPuzzleToCsvLine(puzzle=puzzle,
                                                   pack_title='Pack')
    expected = 'Name,Cipher,Soln,Clue,Pack'
    self.assertEqual(expected, csv)

  def testConvertPuzzleToCsvLineWithQuotesAndCommas(self):
    str_for_quoting = 'a,b'
    puzzle = {'name': str_for_quoting,
              'short_clue': str_for_quoting,
              'solution_text': str_for_quoting,
              'cipher_text': str_for_quoting}
    csv = parse_puzzle_pack.ConvertPuzzleToCsvLine(puzzle=puzzle,
                                                   pack_title=str_for_quoting)
    expected = '"a,b","a,b","a,b","a,b","a,b"'
    self.assertEqual(expected, csv)

  def testEscapeCsvFieldOnStringContainingInnerQuotes(self):
    self.assertEqual('a"b"c', parse_puzzle_pack.EscapeCsvField('a"b"c'))

  def testEscapeCsvFieldOnStringContainingQuoteAtEnd(self):
    # This does not require surrounding the whole string in quotes.
    self.assertEqual('a"b"', parse_puzzle_pack.EscapeCsvField('a"b"'))

  def testEscapeCsvFieldOnStringContainingQuoteAtBeginning(self):
    # This requires surrounding the whole string in quotes.
    self.assertEqual('"""a""b"', parse_puzzle_pack.EscapeCsvField('"a"b'))
    
  def testEscapeCsvFieldOnStringContainingQuotesAtBeginningAndEnd(self):
    self.assertEqual('"""a"""', parse_puzzle_pack.EscapeCsvField('"a"'))

  def testEscapeCsvFieldOnStringContainingCommas(self):
    self.assertEqual('"a,b, c"', parse_puzzle_pack.EscapeCsvField('a,b, c'))

  def testSwapSolutionAndCipher(self):
    puzzle_frag = {'solution_text': 'cipher_oops_haha',
                   'cipher_text': 'soln_oops_haha'}
    puzzle2 = parse_puzzle_pack.SwapSolutionAndCipher(puzzle_frag)
    self.assertEqual('soln_oops_haha', puzzle2['solution_text'])
    self.assertEqual('cipher_oops_haha', puzzle2['cipher_text'])


if __name__ == '__main__':
  unittest.main()