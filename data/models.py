#!/usr/bin/env python

from google.appengine.ext import db


class PackOfPuzzles(db.Model):
  """Container for the puzzles in one of Julia's books."""
  thumbnail_url_part = db.StringProperty()  # the part after images/
  title = db.StringProperty()
  puzzles = db.ListProperty(db.Key)
  introduction = db.TextProperty()
  price_cents = db.IntegerProperty()


class Puzzle(db.Model):
  name = db.StringProperty()  # Usually a number such as 8
  cipher_text = db.StringProperty(multiline=True)
  solution_text = db.StringProperty(multiline=True)
  short_clue = db.StringProperty()                # Such as "d is b"


class UserInfo(db.Model):
  user = db.UserProperty()
  purchased_pack_keys = db.ListProperty(db.Key)
  solved_puzzle_keys = db.ListProperty(db.Key)


class PuzzleOfTheDay(db.Model):
  """There should only be one object of this type."""
  puzzle = db.ReferenceProperty(Puzzle)

