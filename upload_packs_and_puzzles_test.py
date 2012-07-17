#!/usr/bin/env python
import upload_packs_and_puzzles as uploading
import unittest

class UploadingTestCase(unittest.TestCase):
  def testConvertPackFilenameToTitle_OnEmptyCase(self):
    self.assertEquals('', uploading.ConvertPackFilenameToTitle(''))

  def testConvertPackFilenameToTitle_OnSimpleFilename(self):
    self.assertEquals('Foggy Places',
                      uploading.ConvertPackFilenameToTitle('foggy_places.pack'))

  def testConvertPackFilenameToTitleWithPacksDirPrefix(self):
    self.assertEquals('Foggy Places',
                      uploading.ConvertPackFilenameToTitle('packs/foggy_places.pack'))

  def testMakeCommandForUploadingPackDescriptions(self):
    cmd = uploading.MakeCommandForUploadingPackDescriptions('localhost:8080')
    expected = ('bulkload_client.py --url=http://localhost:8080/load_pack_descriptions '
                '--kind=PackOfPuzzles '
                '--filename packs/pack_descriptions.csv')
    self.assertEquals(expected, cmd)

  def testMakeCommandForUploadingPackWithMissingExtension(self):
    try:
      filename_with_missing_csv = 'packs/country_capital_cryptos'
      uploading.MakeCommandForUploadingPackCsv('localhost:8080',
                                               filename_with_missing_csv)
      self.fail('Expected an exception for missing csv extension.')
    except ValueError:
      pass # OK

  def testMakeCommandForUploadingPackCsvOnCountryCapitals(self):
    cmd = uploading.MakeCommandForUploadingPackCsv('localhost:8080',
                                                   'packs/country_capital_cryptos.csv')
    expected = ('bulkload_client.py --url=http://localhost:8080/load_puzzles '
                '--kind=Puzzle '
                '--filename packs/country_capital_cryptos.csv')
    self.assertEquals(expected, cmd)

  def testMakeCommandForUploadingPackCsvOnPresidentsAtAppspot(self):
    cmd = uploading.MakeCommandForUploadingPackCsv('swyzl.appspot.com',
                                                   'packs/presidents.csv')
    expected = ('bulkload_client.py --url=http://swyzl.appspot.com/load_puzzles '
                '--kind=Puzzle '
                '--filename packs/presidents.csv')
    self.assertEquals(expected, cmd)

if __name__ == '__main__':
  unittest.main()
