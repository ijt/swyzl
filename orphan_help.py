'''Handles the /orphans action.'''

import swyzl_models as models


def Main(out):
    orphans = models.GetOrphanPuzzles()
    num_added = models.AddOrphanPuzzlesToTheirPacks(orphans)
    out.write('%s of %s orphaned puzzles found new homes' % (num_added,
                                                             len(orphans)))


if __name__ == '__main__':
    import sys
    Main(sys.stdout)
