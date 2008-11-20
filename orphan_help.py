import swyzl_models as models

from google.appengine.ext import db


def Main():
  orphans = models.GetOrphanPuzzles()
  num_added = models.AddOrphanPuzzlesToTheirPacks(orphans)
  print '%s of %s orphaned puzzles found new homes' % (num_added, len(orphans))


if __name__ == '__main__':
  Main()
