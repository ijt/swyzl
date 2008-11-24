#!/usr/bin/env python
# TODO(ijt): change name to datastore.py

from google.appengine.ext import db


class NotFoundError(Exception):
    pass


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
  pack_title = db.StringProperty()  # Makes bulk upload easier to implement


class UserInfo(db.Model):
  user = db.UserProperty()
  purchased_pack_keys = db.ListProperty(db.Key)
  solved_puzzle_keys = db.ListProperty(db.Key)


class PuzzleOfTheDay(db.Model):
  """There should only be one object of this type."""
  puzzle = db.ReferenceProperty(Puzzle)


def AddOrphanPuzzlesToTheirPacks(orphans):
  num_added = 0
  for o in orphans:
    pack_title = o.pack_title
    pack = PackOfPuzzles.gql('WHERE title = :1', pack_title).get()
    if pack:
      pack.puzzle_keys.append(o.key())
      pack.put()
      num_added += 1
  return num_added

def GetAllPuzzlePacks(max_count=100):
  """Returns all the puzzle packs with puzzle objects, not just keys.
     
  TODO(ijt) see if this too CPU intensive.
  
  Each returned pack object has new fields:
    puzzles: list of puzzle objects
    count: how many puzzles
  
  Each puzzle object is augmented with a relative_url field.

  Args:
    max_count: (optional int) how many packs to get at most
  """
  packs = PackOfPuzzles.all().order('title').fetch(max_count)
  for pack in packs:
    pack.puzzles = [db.get(key) for key in pack.puzzle_keys]
    pack.count = len(pack.puzzle_keys)
    for puzzle in pack.puzzles:
      puzzle.relative_url = '/puzzle/%s' % puzzle.key()
  return packs


def GetOrphanPuzzles():
  orphans = []
  for puzzle in Puzzle.all().fetch(1000):
    try:
      _ = GetPackForPuzzle(puzzle)
    except ValueError:
      orphans.append(puzzle)
  return orphans


def GetPackForPuzzle(puzzle):
  """Returns the PackOfPuzzles containing a given Puzzle."""
  packs = PackOfPuzzles.all().fetch(100)
  for pack in packs:
    if puzzle.key() in pack.puzzle_keys:
      return pack
  msg = 'Could not find a pack containing puzzle %s ' % puzzle.key()
  raise ValueError(msg)


def GetPuzzleOfTheDay():
  """Returns the Puzzle for today."""
  try:
    [potd] = PuzzleOfTheDay.all().fetch(1)
    return db.get(potd.puzzle.key())
  except ValueError:
    raise NotFoundError('There is no puzzle of the day')


def SetPuzzleOfTheDay(puzzle):
  for potd in PuzzleOfTheDay.all().fetch(100):
    potd.delete()
  potd = PuzzleOfTheDay(puzzle=puzzle.key())
  potd.put()
