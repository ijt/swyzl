from google.appengine.ext import bulkload
from google.appengine.api import datastore_types


class PackDescriptionsLoader(bulkload.Loader):
  def __init__(self):
    bulkload.Loader.__init__(self, 'PackOfPuzzles',
                             [('title', str),
                              ('thumbnail_url_part', str),
                              ('introduction', str)])


if __name__ == '__main__':
  bulkload.main(PackDescriptionsLoader())
