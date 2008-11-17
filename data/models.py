#!/usr/bin/env python

from google.appengine.ext import db


class PackOfPuzzles(db.Model):
  """Container for the puzzles in one of Julia's books."""
  thumbnail_url_part = db.StringProperty()  # the part after images/
  title = db.StringProperty()
  puzzle_keys = db.ListProperty(db.Key)  # fixme: should be puzzle_keys
  introduction = db.TextProperty()
  price_cents = db.IntegerProperty()


class Puzzle(db.Model):
  name = db.StringProperty()  # Usually a number such as 8
  cipher_text = db.StringProperty(multiline=True)
  solution_text = db.StringProperty(multiline=True)
  short_clue = db.StringProperty()  # Such as "d is b"


class UserInfo(db.Model):
  user = db.UserProperty()
  purchased_pack_keys = db.ListProperty(db.Key)
  solved_puzzle_keys = db.ListProperty(db.Key)


class PuzzleOfTheDay(db.Model):
  """There should only be one object of this type."""
  puzzle = db.ReferenceProperty(Puzzle)


def GetAllPuzzlePacks(max_count=100):
  """Returns all the puzzle packs with puzzle objects, not just keys.
  
  TODO(ijt) see if this too CPU intensive.
  
  Args:
    max_count: (optional int) how many packs to get at most
  """
  packs = PackOfPuzzles.all().order('title').fetch(max_count)
  for pack in packs:
    pack.puzzles = [db.get(key) for key in pack.puzzle_keys]
    pack.count = len(pack.puzzle_keys)
  return packs
