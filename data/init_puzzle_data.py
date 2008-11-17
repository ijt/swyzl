import models

# Remove all the puzzle data first, to get rid of the old version if any.
for book in models.PuzzleBook.all().fetch(1000):
  book.delete()
for puzzle in models.Puzzle.all().fetch(1000):
  puzzle.delete()
for riddle in models.Riddle.all().fetch(1000):
  riddle.delete()

# Then add the new stuff.
import space
import parks1

# TODO: Test the puzzles to make sure they're consistent.

