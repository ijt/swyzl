from webtest import TestApp
from data import models 

import logging
import main_view
import re
import unittest

from google.appengine.ext import db
from google.appengine.ext import webapp

class MockPuzzleViewer(object):
  def __init__(self):
    self.puzzle = None
    self.title = None
  def ShowPuzzle(self, title, puzzle, request, response):
    self.puzzle = puzzle
    self.title = title


class TestWithNoData(unittest.TestCase):
  def testLoadPuzzles(self):
    app = TestApp(main_view.application)
    response = app.get('/load_puzzles')
    self.assertEqual('200 OK', response.status)
    [pack] = models.GetAllPuzzlePacks()
    self.assertTrue(pack.count >= 1)


class TestWithTwoPuzzlesAndOnePack(unittest.TestCase):
  def setUp(self):
    self.puzzle1 = models.Puzzle(
        name='1',
        solution_text="IN FOG, SUN, OR RAIN YOU CAN LOOK FOR AGATES ON",
        cipher_text  ="EA XCB, VSA, CM MQEA GCS WQA HCCZ XCM QBQNLV CA",
        short_clue="E is I")
    self.puzzle2 = models.Puzzle(
        name='2',
        solution_text="THE TIDES MOVE IN AND OUT OVER TIDE POOLS, RICH",
        cipher_text  ="GYS GMWSK BFZS ME VEW FOG FZSC GMWS HFFQK, CMNY",
        short_clue="S is E")
    self.puzzle1.put()
    self.puzzle2.put()
    self.puzzle_pack = models.PackOfPuzzles(
        title="Pack of Joy",
        puzzle_keys=[self.puzzle1.key(), self.puzzle2.key()])
    self.puzzle_pack.put()
    
  def testThatGettingPuzzlesUsingDbGetWorks(self):
    [puzzle1, puzzle2] = [db.get(key) for key in self.puzzle_pack.puzzle_keys]
    self.assertEqual(self.puzzle1.key(), puzzle1.key())
    self.assertEqual(self.puzzle2.key(), puzzle2.key())

  def testDefaultPage(self):
    app = TestApp(main_view.application)
    response = app.get('/')
    self.assertEqual('200 OK', response.status)
    self.assertTrue('Puzzle Packs' in response)

  def testPlayPuzzleOfTheDayWhenNoneIsSpecified(self):
    app = TestApp(main_view.application)
    main_view.puzzle_viewer = MockPuzzleViewer()
    default_puzzle = main_view.GetDefaultPuzzle()
    response = app.get('/potd')
    self.assertEqual('200 OK', response.status)
    self.assertTrue(isinstance(default_puzzle, models.Puzzle))
    self.assertTrue(isinstance(main_view.puzzle_viewer.puzzle, models.Puzzle))
    self.assertEqual(default_puzzle.key(), main_view.puzzle_viewer.puzzle.key())

  def testPlayPuzzleOfTheDay(self):
    potd = models.PuzzleOfTheDay(puzzle=self.puzzle2)
    potd.put()
    self.assertEqual(self.puzzle2.key(), potd.puzzle.key())
    app = TestApp(main_view.application)
    main_view.puzzle_viewer = MockPuzzleViewer()
    response = app.get('/potd')
    self.assertEqual('200 OK', response.status)
    self.assertEqual(potd.puzzle.key(), main_view.puzzle_viewer.puzzle.key())
    self.assertTrue(potd.puzzle.name in main_view.puzzle_viewer.title)

  def testThatGetAllPuzzlePacksReturnsOurPackAndFilledOutPuzzleObjects(self):
    [pack] = models.GetAllPuzzlePacks()
    self.assertEqual(self.puzzle_pack.key(), pack.key())
    self.assertEqual(2, pack.count)
    [puzzle1, puzzle2] = pack.puzzles
    self.assertEqual('1', puzzle1.name)
    self.assertEqual('2', puzzle2.name)

  def testThatTheLinksToPuzzlesAreValid(self):
    app = TestApp(main_view.application)
    [pack] = models.GetAllPuzzlePacks()
    [puzzle1, puzzle2] = pack.puzzles
    for puzzle in pack.puzzles:
      response = app.get(puzzle1.relative_url)
      self.assertEqual('200 OK', response.status)

  def testThatPuzzlesGetValidTitlesForDisplay(self):
    puzzle = self.puzzle1
    pack = self.puzzle_pack
    title_for_display = main_view.MakePuzzleTitleForDisplay(puzzle)
    rx = '.*%s.*%s.*' % (pack.title, puzzle.name)
    self.assertTrue(re.compile(rx).match(title_for_display))

  def testDefaultPage(self):
    def MockWriteTemplate(request, response, filename, params):
      [pack] = params['packs']
      self.assertEqual(2, len(pack.puzzles))
      self.assertTrue(isinstance(pack.title, (str, unicode)))
      self.assertTrue(isinstance(pack.count, (int, long)))
      for puzzle in pack.puzzles:
        self.assertTrue(isinstance(puzzle.name, (str, unicode)))
    saved_write_template = main_view.WriteTemplate
    main_view.WriteTemplate = MockWriteTemplate
    app = TestApp(main_view.application)
    main_view.puzzle_viewer = MockPuzzleViewer()
    response = app.get('/')
    self.assertEqual('200 OK', response.status)
    main_view.WriteTemplate = saved_write_template

