import utils
import unittest


class TestUtils(unittest.TestCase):

    def assertDictEqual(self, a, b):
        for key in a:
            self.assertEqual(a[key], b[key])
        for key in b:
            self.assertEqual(b[key], a[key])

    def testMakeEncryptionMap(self):
        self.assertDictEqual({}, utils.MakeEncryptionMap('', ''))

        self.assertDictEqual({'a': 'b'}, utils.MakeEncryptionMap('a', 'b'))
        self.assertDictEqual({'a': 'b'}, utils.MakeEncryptionMap('aa', 'bb'))
        self.assertDictEqual({'a': 'b', 'b': 'c'}, utils.MakeEncryptionMap('ab', 'bc'))
        self.assertDictEqual({'a': 'b'}, utils.MakeEncryptionMap("a.,'", "b.,'"))
        self.assertRaises(ValueError, utils.MakeEncryptionMap, 'aa', 'bc')
        self.assertRaises(ValueError, utils.MakeEncryptionMap, 'a', 'bc')
        self.assertRaises(ValueError, utils.MakeEncryptionMap, '.', 'bq')

        # Spaces, commas, apostrophes, and periods should map to themselves.
        for x in [' ', ',', "'", '.']:
            self.assertDictEqual({}, utils.MakeEncryptionMap(x, x))
            self.assertRaises(ValueError, utils.MakeEncryptionMap, x, 'a')

    def testCheckPuzzle(self):
        utils.CheckPuzzle('', '')
        utils.CheckPuzzle('a', 'a')
        utils.CheckPuzzle('a', 'b')
        utils.CheckPuzzle('ab', 'ab')
        utils.CheckPuzzle('ab', 'bc')

        # Spaces, commas, apostrophes, and periods should map to themselves.
        for x in [' ', ',', "'", '.']:
            utils.CheckPuzzle(x, x)
            self.assertRaises(ValueError, utils.CheckPuzzle, x, 'a')
            self.assertRaises(ValueError, utils.CheckPuzzle, 'a', x)

    def testMakeRandomLetterMap(self):
        lmap = utils.MakeRandomLetterMap()
        self.assertEquals(26, len(lmap))
        chars = set(lmap.values())
        self.assertEquals(26, len(chars))
        for c in chars:
            self.assertTrue(ord('A') <= ord(c) <= ord('Z'))

    def testMakeRandomLetterMapForLettersIn_EmptyCase(self):
        self.assertDictEqual({}, utils.MakeRandomLetterMapForLettersIn(''))

    def testMakeRandomLetterMapForLettersIn(self):
        message = 'ACDEFGHIJK . , !! LMNOPQRSTUVWXYZ'
        my_map = utils.MakeRandomLetterMapForLettersIn(message)
        self.assertEquals(25, len(my_map))
        self.assertEquals(25, len(set(my_map.values())))
        self.assertEquals(25, len(set(my_map.keys())))

    def testConvertStringToEncodingMap(self):
        self.assertDictEqual({}, utils.ConvertStringToEncodingMap(''))
        self.assertDictEqual({'A': 'B'}, utils.ConvertStringToEncodingMap('AB'))
        self.assertDictEqual({'A': 'B', 'D': 'C'},
                                                 utils.ConvertStringToEncodingMap('ABDC'))
        self.assertDictEqual({'P': 'Z', 'A': 'B', 'D': 'C'},
                                                 utils.ConvertStringToEncodingMap('PZABDC'))

    def testGetLetters(self):
        self.assertEquals(set(), utils.GetLetters(''))
        self.assertEquals(set(), utils.GetLetters(' '))
        self.assertEquals(set(), utils.GetLetters(' !,.<>12341@#$!@#$^%^&()'))
        self.assertEquals(set(['A']), utils.GetLetters('A'))
        self.assertEquals(set(['A', 'B']), utils.GetLetters('ABA'))
        self.assertEquals(set(['D', 'P', 'Q', 'S']), utils.GetLetters('DPSD ,.DQS'))

    def testGenerateWordHtmls_emptyCase(self):
        self.assertEqual([], utils.GenerateWordHtmls([]))

    def testGenerateWordHtmls_semiEmptyCase(self):
        expected = ['<table class="boxOnLetter"><tr><td></td></tr>'
                                '<tr><td class="letter"></td></tr></table>']
        self.assertEqual(expected, utils.GenerateWordHtmls(['']))

    def testGenerateWordHtmls(self):
        result = utils.GenerateWordHtmls(['ab', 'b'])
        for part in result:
            self.assertTrue('<table' in part)
            self.assertTrue('</table>' in part)
            self.assertTrue('>b<' in part)


if __name__ == '__main__':
        unittest.main()
