#!/usr/bin/env python2.4
import sys
import utils


def EnsurePeriod(s):
  """Makes sure a string ends with a period."""
  if s.endswith('.'):
    return s
  else:
    return s + '.'


def ParseString(string):
  """Extracts puzzles from a string."""
  lines = string.split('\n')
  lines = [line.strip() for line in lines]  # remove whitespace
  lines = [line for line in lines if line]  # remove blank lines
  result = []
  for i in xrange(len(lines) / 4):
    i4 = i * 4
    puzzle = {
      'name': lines[i4],
      'short_clue': lines[i4 + 1],
      'solution_text': lines[i4 + 2],
      'cipher_text': lines[i4 + 3]
    }
    puzzle['short_clue'] = EnsurePeriod(puzzle['short_clue'])
    try:
      utils.CheckPuzzle(puzzle['solution_text'], puzzle['cipher_text'])
    except ValueError, e:
      raise ValueError('Error on puzzle %s: %s' % (puzzle['name'], str(e)))
    result.append(puzzle)
  return result
  

if __name__ == '__main__':
  try:
    filename = sys.argv[1]
  except:
    print 'Usage: parse_puzzle_pack.py filename'
    sys.exit(1)
  contents = open(filename).read()
  try:
    puzzles = ParseString(contents)
  except ValueError, e:
    print str(e)
    sys.exit(1)
  print 'Successfully checked %s puzzles.' % len(puzzles)


