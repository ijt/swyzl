import orphan_help
import swyzl_models as models

import unittest

from google.appengine.ext import db


class OrphansEmptyTestCase(unittest.TestCase):
  def testMain(self):
    orphan_help.Main()

  def testGetOrphans(self):
    self.assertEqual(0, len(models.GetOrphanPuzzles()))

  def testAddOrphans(self):
    self.assertEqual(0, models.AddOrphanPuzzlesToTheirPacks([]))


class OrphansTestCase(unittest.TestCase):
  def setUp(self):
    title = 'my pack'
    self.puzzle = models.Puzzle()
    self.orphan_puzzle = models.Puzzle(pack_title=title)
    self.orphan_with_bad_name = models.Puzzle(pack_title='')
    self.puzzle.put()
    self.orphan_puzzle.put()
    self.orphan_with_bad_name.put()
    self.pack = models.PackOfPuzzles(title=title,
                                     puzzle_keys=[self.puzzle.key()])
    self.pack.put()

  def testGetOrphans(self):
    [orphan1, orphan2] = models.GetOrphanPuzzles()
    self.assertEqual(self.orphan_puzzle.key(), orphan1.key())
    self.assertEqual(self.orphan_with_bad_name.key(), orphan2.key())

  def testAddOrphans(self):
    orphans = [self.orphan_with_bad_name, self.orphan_puzzle]
    # Only one orphan has a valid pack name, so the return value is 1.
    self.assertEqual(1, models.AddOrphanPuzzlesToTheirPacks(orphans))
    self.pack = models.PackOfPuzzles.all().get()
    self.assertEqual(2, len(self.pack.puzzle_keys))
    self.assertEqual(self.orphan_puzzle.key(), self.pack.puzzle_keys[1])
    

  def testMain(self):
    self.assertEqual(1, len(self.pack.puzzle_keys))
    orphan_help.Main()
    self.pack = models.PackOfPuzzles.all().get()
    self.assertEqual(2, len(self.pack.puzzle_keys))
    self.assertEqual(self.orphan_puzzle.key(), self.pack.puzzle_keys[1])
