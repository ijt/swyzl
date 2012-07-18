#!/usr/bin/env python

import pack_parsing
import unittest


class ParsePuzzlePackTestCase(unittest.TestCase):
    def testEmptyCase(self):
        self.assertEqual([], pack_parsing.ParseString(''))

    def testOnOneGoodPuzzle(self):
        file_string = '''

        1
        Z is E.
        I'm feeling puzzled.
        J'n gzzmjoh qvaamze.

        '''
        [puzzle] = pack_parsing.ParseString(file_string)
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
        [puzzle1, puzzle2] = pack_parsing.ParseString(file_string)
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
            pack_parsing.ParseString(file_string)
            self.fail('Expected a value error on incorrect puzzle.')
        except ValueError, e:
            self.assertTrue('puzzle 1' in str(e).lower())

    def testConvertPuzzleToCsvLine_EmptyCase(self):
        puzzle = {'name': '',
                  'short_clue': '',
                  'solution_text': '',
                  'cipher_text': ''}
        csv = pack_parsing.ConvertPuzzleToCsvLine(puzzle=puzzle,
                                                  pack_title='')
        expected = ',,,,'
        self.assertEqual(expected, csv)

    def testConvertPuzzleToCsvLineWithQuotesAndCommas(self):
        str_for_quoting = 'a,b'
        puzzle = {'name': str_for_quoting,
                  'short_clue': str_for_quoting,
                  'solution_text': str_for_quoting,
                  'cipher_text': str_for_quoting}
        csv = pack_parsing.ConvertPuzzleToCsvLine(puzzle=puzzle,
                                                  pack_title=str_for_quoting)
        expected = '"a,b","a,b","a,b","a,b","a,b"'
        self.assertEqual(expected, csv)

    def testEscapeCsvFieldOnStringContainingInnerQuotes(self):
        self.assertEqual('a"b"c', pack_parsing.EscapeCsvField('a"b"c'))

    def testEscapeCsvFieldOnStringContainingQuoteAtEnd(self):
        # This does not require surrounding the whole string in quotes.
        self.assertEqual('a"b"', pack_parsing.EscapeCsvField('a"b"'))

    def testEscapeCsvFieldOnStringContainingQuoteAtBeginning(self):
        # This requires surrounding the whole string in quotes.
        self.assertEqual('"""a""b"', pack_parsing.EscapeCsvField('"a"b'))

    def testEscapeCsvFieldOnStringContainingQuotesAtBeginningAndEnd(self):
        self.assertEqual('"""a"""', pack_parsing.EscapeCsvField('"a"'))

    def testEscapeCsvFieldOnStringContainingCommas(self):
        self.assertEqual('"a,b, c"', pack_parsing.EscapeCsvField('a,b, c'))


class TestCaseWithFakePuzzle(unittest.TestCase):
    def setUp(self):
        self.puzzle = {'name': 'Name',
                       'short_clue': 'Clue',
                       'solution_text': 'Soln',
                       'cipher_text': 'Cipher'}

    def testConvertPuzzleToCsvLine(self):
        csv = pack_parsing.ConvertPuzzleToCsvLine(puzzle=self.puzzle,
                                                  pack_title='Pack')
        expected = 'Name,Cipher,Soln,Clue,Pack'
        self.assertEqual(expected, csv)


if __name__ == '__main__':
    unittest.main()
