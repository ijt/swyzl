"""This module enables bulk loading of individual puzzles."""

from google.appengine.ext import bulkload


class PuzzlesLoader(bulkload.Loader):
    def __init__(self):
        bulkload.Loader.__init__(self, 'Puzzle',
                                 [('name', str),
                                  ('cipher_text', str),
                                  ('solution_text', str),
                                  ('short_clue', str),
                                  ('pack_title', str)])


if __name__ == '__main__':
    bulkload.main(PuzzlesLoader())
