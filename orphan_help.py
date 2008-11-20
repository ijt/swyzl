import swyzl_models as models

from google.appengine.ext import db


def Main():
  orphans = models.GetOrphanPuzzles()
  models.AddOrphanPuzzlesToTheirPacks(orphans)


if __name__ == '__main__':
  Main()
