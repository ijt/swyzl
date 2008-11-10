from webtest import TestApp
from data import models 

import logging
import main_view
import unittest

from google.appengine.ext import db
from google.appengine.ext import webapp

class MockPuzzleViewer(object):
  def __init__(self):
    self.puzzle = None
  def ShowPuzzle(self, puzzle, request, response):
    self.puzzle = puzzle

class IndexTest(unittest.TestCase):

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

