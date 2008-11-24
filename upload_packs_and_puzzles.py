#!/usr/bin/env python2.5

import pack_parsing


class Error(Exception):
  pass


def DoSystemCall(command):
  """Runs a system call and throws an exception (Error) if it fails."""
  if os.system(command):
    raise Error('Command failed: %s' % command)


def ConvertPackFilenameToTitle(pack_filename):
  """Converts pack filenames to pack titles.
  
  For example, 'country_capital_cryptos' becomes 'Country Capital Cryptos'.
  """
  import re
  basename = re.compile(r'\.pack').sub('', pack_filename)
  return ' '.join([part.capitalize() for part in basename.split('_')])


def MakeCommandForUploadingPackDescriptions(hostname):
  """Makes a unix command to upload the pack descriptions CSV file."""
  return ('bulkload_client.py --url=http://%s/load_pack_descriptions '
          '--kind=PackOfPuzzles '
          '--filename packs/pack_descriptions.csv' % hostname)


def MakeCommandForUploadingPackCsv(hostname, pack_csv_filename):
  """Makes a unix command to upload the puzzles for a pack."""
  if not pack_csv_filename.endswith('.csv'):
    raise ValueError('pack_csv_filename should end with .csv')
  return ('bulkload_client.py --url=http://%s/load_puzzles '
          '--kind=Puzzle '
          '--filename %s' % (hostname, pack_csv_filename))


def Main(hostname, pack_filenames):
  # TODO(ijt): Run a command to clear the data store of puzzles and packs.
  
  # Bulk upload the pack descriptions.
  command = MakeCommandForUploadingPackDescriptions(hostname)
  DoSystemCall(command)
  for pack_filename in pack_filenames:
    title = ConvertPackFilenameToTitle(pack_filename)
    pack_parsing.ConvertPackFileToCsv(pack_filename, title)
    pack_csv_name = os.path.splitext(pack_filename)[0] + '.csv'
    command = MakeCommandForUploadingPackCsv(hostname, pack_csv_name)
    DoSystemCall(command)


if __name__ == '__main__':
  import glob
  try:
    hostname = sys.argv[1]
  except:
    print 'Usage: upload_packs_and_puzzles.py hostname'
  Main(hostname, pack_filenames=glob.glob('packs/*.pack'))
