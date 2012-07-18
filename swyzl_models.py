"""AppEngine data store models for Swyzl data, and operations on the models"""

from google.appengine.ext import db


class NotFoundError(Exception):
    pass


class PackOfPuzzles(db.Model):
    """Container for all the puzzles in one of Julia's books"""
    thumbnail_url_part = db.StringProperty()    # the part after images/
    index = db.IntegerProperty()
    title = db.StringProperty()
    puzzle_keys = db.ListProperty(db.Key)
    introduction = db.TextProperty()
    price_cents = db.IntegerProperty()


class Puzzle(db.Model):
    """Cryptogram puzzle"""
    name = db.StringProperty()    # Index of the puzzle in its book
    cipher_text = db.StringProperty(multiline=True)
    solution_text = db.StringProperty(multiline=True)
    short_clue = db.StringProperty()    # Such as "d is b"
    pack_title = db.StringProperty()    # Makes bulk upload easier to implement


class UserInfo(db.Model):
    """App-specific user data, including which puzzles the user has solved"""
    user = db.UserProperty()
    solved_puzzle_keys = db.ListProperty(db.Key)


def AddOrphanPuzzlesToTheirPacks(orphans):
    """
    Given a list of orphan puzzles (ones not found in any packs), add them to
    the packs to which they say they belong.

    @param orphans: the orphans to add
    @type  orphans: list of Puzzle
    """
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
    """
    Return all the puzzle packs with puzzle objects, not just keys.

    Each returned pack object has new fields:
        puzzles: list of puzzle objects
        count: how many puzzles

    Each puzzle object is augmented with a relative_url field.

    @param max_count: how many packs to get at most
    @type  max_count: int
    """
    packs = PackOfPuzzles.all().order('index').fetch(max_count)
    for pack in packs:
        pack.puzzles = [db.get(key) for key in pack.puzzle_keys]
        pack.puzzles = sorted(pack.puzzles, key=lambda p: int(p.name))
        pack.count = len(pack.puzzle_keys)
        for puzzle in pack.puzzles:
            puzzle.relative_url = '/puzzle/%s/%s' % (pack.index, puzzle.name)
    return packs


def GetOrphanPuzzles():
    """
    Find all puzzles that don't have an associated pack.

    @rtype: list of Puzzle
    """
    orphans = []
    for puzzle in Puzzle.all().fetch(1000):
        try:
            GetPackForPuzzle(puzzle)
        except ValueError:
            orphans.append(puzzle)
    return orphans


def GetPackForPuzzle(puzzle):
    """
    Get the PackOfPuzzles containing a given Puzzle.

    @param puzzle: puzzle for which to find a pack
    @type  puzzle: Puzzle
    @rtype: list of PackOfPuzzles
    """
    packs = PackOfPuzzles.all().fetch(100)
    for pack in packs:
        if puzzle.key() in pack.puzzle_keys:
            return pack
    msg = 'Could not find a pack containing puzzle %s ' % puzzle.key()
    raise ValueError(msg)


def GetPuzzle(pack_title, name):
    """
    Get the puzzle with a given pack title and name

    @param pack_title: title of the pack containing the puzzle
    @type  pack_title: str
    @param name: name of the puzzle, usually numerical such as '10'
    @type  name: str
    @rtype: Puzzle
    """
    query = Puzzle.gql('WHERE pack_title = :pack_title AND name = :name',
        pack_title=pack_title, name=name)
    return query.get()


def GetPack(index):
    """
    Get a Pack for a given 1-based index.

    @param index: index of the pack
    @type  index: int
    @rtype: PackOfPuzzles
    """
    return PackOfPuzzles.gql('WHERE index = :index', index=int(index)).get()
