#!/usr/bin/env python2.4
import getopt
import re
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
  comment_rx = re.compile('#.*')
  lines = [comment_rx.sub('', line) for line in lines]  # remove comments
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


def EscapeCsvField(field):
  if field.find(',') != -1 or field.startswith('"'):
    field = field.replace('"', '""')  # Replace double quotes with pairs of them.
    field = '"%s"' % field
  return field


def ConvertPuzzleToCsvLine(puzzle, pack_title):
  """Converts a dict representing a puzzle to a string of CSV."""
  puzzle = puzzle.copy()
  puzzle.update(pack_title=pack_title)
  for key, val in puzzle.iteritems():
    puzzle[key] = EscapeCsvField(val)
  return ('%(name)s,%(cipher_text)s,%(solution_text)s,'
          '%(short_clue)s,%(pack_title)s' % puzzle)


def SwapSolutionAndCipher(puzzle):
  """Interchanges the solution_text and cipher_text fields of a puzzle dict.
  
  This function was written to help with a file where ijt accidentally
  transposed the solution and cipher lines.
  """
  puzzle = puzzle.copy()
  old_soln = puzzle['solution_text']
  puzzle['solution_text'] = puzzle['cipher_text']
  puzzle['cipher_text'] = old_soln
  return puzzle


def PutPuzzlesIntoPackFormat(puzzles):
  lines = []
  for puzzle in puzzles:
    lines.append(puzzle['name'])
    lines.append(puzzle['short_clue'])
    lines.append(puzzle['solution_text'])
    lines.append(puzzle['cipher_text'])
  return lines



