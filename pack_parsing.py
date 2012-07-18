#!/usr/bin/env python

import re
import utils


def EnsurePeriod(s):
    """Make sure a string ends with a period."""
    if s.endswith('.'):
        return s
    else:
        return s + '.'


def ParseString(string):
    """Extract puzzles from a string."""
    lines = string.split('\n')
    comment_rx = re.compile('#.*')
    lines = [comment_rx.sub('', line) for line in lines]    # remove comments
    lines = [line.strip() for line in lines]    # remove whitespace
    lines = [line for line in lines if line]    # remove blank lines
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
    """
    Replace double quotes with pairs of them.

    @param field: CSV field that may need escaping
    @type  field: str 
    """
    if field.find(',') != -1 or field.startswith('"'):
        field = field.replace('"', '""')
        field = '"%s"' % field
    return field


def ConvertPuzzleToCsvLine(puzzle, pack_title):
    """
    Convert a dict representing a puzzle to a string of CSV.
    
    @param puzzle: puzzle to be converted
    @type  puzzle: dict
    @param pack_title: title of the puzzle's pack
    @type  pack_title: str
    """
    puzzle = puzzle.copy()
    puzzle.update(pack_title=pack_title)
    for key, val in puzzle.iteritems():
        puzzle[key] = EscapeCsvField(val)
    return ('%(name)s,%(cipher_text)s,%(solution_text)s,'
                    '%(short_clue)s,%(pack_title)s' % puzzle)


def ConvertPackFileToCsv(filename, title):
    """
    Convert a pack file to CSV format.

    For example, given a pack file called presidents.pack, calling
    ConvertPackFileToCsv('presidents.pack', pack_name='Presidential Cryptos')
    will generate a new file called presidents.csv suitable for bulk uploading
    to the server.

    @param filename: pack file path
    @type  filename: str
    @param title: title of the pack
    @type  title: str
    """
    puzzles = ParseString(open(filename).read())
    lines = [ConvertPuzzleToCsvLine(p, title) for p in puzzles]
    csv_filename = filename.replace('.pack', '') + '.csv'
    outfile = open(csv_filename, 'w')
    outfile.write('\n'.join(lines))
    outfile.close()

