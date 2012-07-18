#!/usr/bin/env python

"""This module handles all HTTP requests for swyzl."""

import os
import re
import urllib

import wsgiref.handlers

from django.utils import simplejson
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

import swyzl_models as models
import utils


class FakePuzzle(object):
    def __init__(self):
        self.short_clue = 'A is B'
        self.cipher_text = 'A'
        self.solution_text = 'B'
        self.key = 'puzzle_test'

FAKE_PUZZLE = FakePuzzle()


class PuzzleViewer(object):
    """HTML renderer for puzzles"""
    def ShowPuzzle(self, intro, title, puzzle, request, response):
        """Render a puzzle UI to the HTTP response.
        
        @param intro: introduction for the puzzle
        @type  intro: str
        @param title: title for the puzzle
        @type  title: str
        @param puzzle: the puzzle to be shown
        @type  puzzle: swyzl_models.Puzzle
        @param request: HTTP request
        @type  request: AppEngine request
        """
        cipher_words = puzzle.cipher_text.split(' ')
        word_htmls = utils.GenerateWordHtmls(cipher_words)
        params = {'puzzle': puzzle, 'word_htmls': word_htmls, 'title': title,
            'intro': intro}
        WriteTemplate(request, response, 'puzzle.html', params)


def GetDefaultPuzzle():
    """Return the first entered puzzle, or None if there is none."""
    puzzles = models.Puzzle.all().fetch(1)
    return puzzles and puzzles[0] or None


def SubmitNewPuzzle(clear_text, map_as_string, tags_string, short_clue):
    """Save a puzzle to the db.

    @param clear_text: url encoded secret message.
    @type  clear_text: str
    @param map_as_string: like "ABCD" to map A to B and C to D.
    @type  map_as_string: str
    @param tags_string: such as 'first tag,second tag'
    @type  tags_string: str
    @param short_clue: such as 'A is B'
    @type  short_clue: str
    """
    encoding_map = utils.ConvertStringToEncodingMap(map_as_string)
    clear_text = urllib.unquote(clear_text)
    cipher_text = utils.Encrypt(clear_text, encoding_map)
    utils.CheckPuzzle(clear_text, cipher_text)

    puzzle = models.Puzzle()
    puzzle.cipher_text = cipher_text
    puzzle.solution_text = clear_text
    puzzle.author = users.get_current_user()
    puzzle.short_clue = short_clue
    puzzle.put()

    # Add tags
    tag_texts = set(t.strip().lower() for t in tags_string.split(','))
    tag_texts = [t or "untagged" for t in tag_texts]
    for tag_text in tag_texts:
        tag_in_db = models.Tag.gql('WHERE text = :1', tag_text).get()
        if tag_in_db:
            tag_in_db.num_times_used += 1
            tag_in_db.puzzles.append(puzzle.key())
        else:
            # Create a new tag
            tag_in_db = models.Tag(text=tag_text, num_times_used=1,
                                   puzzles=[puzzle.key()])
        tag_in_db.put()


def UpdatePacksInMemcache():
    """Put the latest version of the puzzle packs into memcache."""
    packs = models.GetAllPuzzlePacks()
    memcache.add(key="packs", value=packs, time=24 * 60 * 60)
    return packs


class UpdatePacksInMemcacheHandler(webapp.RequestHandler):
    """Handler for /update"""

    def get(self):
        UpdatePacksInMemcache()
        self.response.out.write('Updated memcache.')


class MainPage(webapp.RequestHandler):
    """Handler for /"""

    def GetUserInfo(self):
        """Get the current user if any and make a link to login or logout.

        @return: (user, url, url_link_text)
        @rtype: (google.appengine.api.users.User, str, str)
        """
        user = users.get_current_user()
        user_info = GetInfoForUser(user)
        if user:
            # Check to see if the user has auxiliary info for Swyzl, and if not
            # then create it.
            if not user_info:
                user_info = models.UserInfo()
                user_info.user = user
                user_info.put()

            url = users.create_logout_url(self.request.uri)
            url_link_text = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_link_text = 'Login'
        return (user, url, url_link_text)

    def get(self):
        """Handle the HTTP GET request."""
        user, url, url_link_text = self.GetUserInfo()
        packs = memcache.get('packs') or UpdatePacksInMemcache()
        params = {
            'log_inout_url': url.replace('&', '&amp;'),
            'log_inout_link_text': url_link_text,
            'packs': packs,
            'user': user
        }
        WriteTemplate(self.request, self.response, 'home.html', params)


class AboutPage(webapp.RequestHandler):
    """Handler for /about"""

    def get(self):
        """Handle an HTTP GET request."""
        WriteTemplate(self.request, self.response, 'about.html', {})


class TipsPage(webapp.RequestHandler):
    """Handler for /tips"""

    def get(self):
        """Handle an HTTP GET request."""
        WriteTemplate(self.request, self.response, 'tips.html', {})


def GetInfoForUser(user):
    return models.UserInfo.gql('WHERE user = :1', user).get()


class MakePuzzleUi(webapp.RequestHandler):
    def post(self):
        puzzle_text = self.request.get('content')
        words = re.compile(r'\s+').split(puzzle_text)
        htmls = utils.GenerateWordHtmls(words)
        html = '\n'.join(htmls) + '<hr />' + utils.GenerateAlphabetUi()
        encoding_map = utils.MakeRandomLetterMapForLettersIn(puzzle_text)
        json = simplejson.dumps(dict(html=html, encodingMap=encoding_map))
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(json)


def MakePuzzleTitleForDisplay(puzzle):
    pack = models.GetPackForPuzzle(puzzle)
    return '%s, Puzzle %s' % (pack.title, puzzle.name)


class PlayPuzzle(webapp.RequestHandler):
    def get(self, book_index, puzzle_index):
        pack = models.GetPack(index=book_index)
        puzzle = models.GetPuzzle(pack_title=pack.title, name=puzzle_index)
        if puzzle:
            title = MakePuzzleTitleForDisplay(puzzle)
            puzzle_viewer.ShowPuzzle(pack.introduction, title, puzzle,
                                     self.request, self.response)
        else:
            self.response.out.write('Puzzle not found!')


class PuzzleTest(webapp.RequestHandler):
    def get(self):
        puzzle_viewer.ShowPuzzle('Easy Puzzle', FAKE_PUZZLE, self.request,
                                 self.response)


class SubmitNewPuzzleHandler(webapp.RequestHandler):
    def get(self):
        try:
            clear_text = self.request.get('message').upper()
            map_as_string = self.request.get('encoding_map').upper()
            tags_string = self.request.get('tags').upper()
            short_clue = self.request.get('short_clue')
            SubmitNewPuzzle(clear_text, map_as_string, tags_string, short_clue)
        except ValueError, e:
            self.response.out.write(str(e))


class Encrypt(webapp.RequestHandler):
    def get(self):
        message = urllib.unquote(self.request.get('message'))
        self.response.headers['Content-Type'] = 'text/plain'
        letter_map = utils.MakeRandomLetterMap()
        self.response.out.write(utils.Encrypt(message=message,
                                              letter_map=letter_map))


class DoneWithPuzzle(webapp.RequestHandler):
    def get(self):
        puzzle_id = self.request.get('puzzle_id')
        user_solution = self.request.get('solution').upper()
        puzzle = (FAKE_PUZZLE if puzzle_id == 'puzzle_test'
                  else db.get(puzzle_id))
        # Remove spaces since the user solution also has its spaces removed.
        # Also remove punctuation.
        real_solution = ''.join(c for c in puzzle.solution_text if c.isalpha())

        if user_solution == real_solution:
            # Add this puzzle to the list of puzzles this user has solved.
            user = users.get_current_user()
            if user:
                user_info = models.UserInfo.gql('WHERE user = :1', user).get()
                user_info.solved_puzzle_keys.append(puzzle.key())
                user_info.put()
            self.response.out.write('Yes!')
        else:
            self.response.out.write('Try again.')


class BuyNowExperiment(webapp.RequestHandler):
    def get(self):
        WriteTemplate(self.request, self.response, 'bn.html', {})


class NotFound(webapp.RequestHandler):
    def get(self):
        self.response.out.write("There's nothing to see here. How 'bout a "
                                "<a href='/'>puzzle</a>?")


class ClearPuzzles(webapp.RequestHandler):
    def get(self):
        puzzles = models.Puzzle.all().fetch(10000)
        for puzzle in puzzles:
            puzzle.delete()
        self.response.out.write('Deleted %s puzzles.' % len(puzzles))


class ClearPacks(webapp.RequestHandler):
    def get(self):
        packs = models.PackOfPuzzles.all().fetch(10000)
        for pack in packs:
            pack.delete()
        self.response.out.write('Deleted %s packs.' % len(packs))


def WriteTemplate(request, response, template_name, params,
                  mime_type='text/html'):
    '''Shows a template with some parameters'''
    path = os.path.join(os.path.dirname(__file__), 'templates/%s' %
                        template_name)
    response.headers['Content-Type'] = mime_type
    response.out.write(template.render(path, params))


urls_to_handlers = [('/', MainPage),
                    ('/update', UpdatePacksInMemcacheHandler),
                    ('/about', AboutPage),
                    ('/buynow', BuyNowExperiment),
                    ('/done_with_puzzle', DoneWithPuzzle),
                    ('/encrypt', Encrypt),
                    ('/make_puzzle_ui', MakePuzzleUi),    # makes a puzzle ui
                    ('/puzzle/(\d+)/(\d+)', PlayPuzzle),
                    ('/puzzle_test', PuzzleTest),
                    ('/tips', TipsPage),

                    # Admin:
                    ('/clear_puzzles', ClearPuzzles),
                    ('/clear_packs', ClearPacks),

                    ('.*', NotFound)]

application = webapp.WSGIApplication(urls_to_handlers, debug=True)
puzzle_viewer = PuzzleViewer()


def Main():
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
    Main()
