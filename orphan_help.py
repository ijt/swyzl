import swyzl_models as models

from google.appengine.ext import db


def Main():
  orphans = models.GetOrphanPuzzles()
  for o in orphans:
    pack = models.PackOfPuzzles.gql('WHERE title = :1', o.pack_title).get()
    pack.puzzle_keys.append(o.key())
    pack.put()


if __name__ == '__main__':
  Main()
