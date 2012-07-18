from google.appengine.ext import bulkload


class PackDescriptionsLoader(bulkload.Loader):
    def __init__(self):
            bulkload.Loader.__init__(self, 'PackOfPuzzles',
                                     [('index', int),
                                      ('title', str),
                                      ('thumbnail_url_part', str),
                                      ('introduction', str)])


if __name__ == '__main__':
    bulkload.main(PackDescriptionsLoader())
