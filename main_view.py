#!/usr/bin/env python

"""This module handles most HTTP requests for swyzl."""

import os
import re

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


class PuzzleViewer(object):
    """HTML renderer for puzzles"""
    def ShowPuzzle(self, intro, title, puzzle, request, response):
        """
        Render a puzzle UI to the HTTP response.
        
        @param intro: introduction for the puzzle
        @type  intro: str
        @param title: title for the puzzle
        @type  title: str
        @param puzzle: the puzzle to be shown
        @type  puzzle: swyzl_models.Puzzle
        @param request: HTTP request
        @type  request: google.appengine.ext.webapp.Request
        """
        cipher_words = puzzle.cipher_text.split(' ')
        word_htmls = utils.GenerateWordHtmls(cipher_words)
        params = {'puzzle': puzzle, 'word_htmls': word_htmls, 'title': title,
            'intro': intro}
        WriteTemplate(response, 'puzzle.html', params)


def GetDefaultPuzzle():
    """Return the first entered puzzle, or None if there is none."""
    puzzles = models.Puzzle.all().fetch(1)
    return puzzles and puzzles[0] or None


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
        """
        Get the current user if any and make a link to login or logout.

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
        WriteTemplate(self.response, 'home.html', params)


class AboutPage(webapp.RequestHandler):
    """Handler for /about"""

    def get(self):
        """Handle an HTTP GET request."""
        WriteTemplate(self.response, 'about.html', {})


class TipsPage(webapp.RequestHandler):
    """Handler for /tips"""

    def get(self):
        """Handle an HTTP GET request."""
        WriteTemplate(self.response, 'tips.html', {})


def GetInfoForUser(user):
    """
    Get app-specific information for a given user.

    @param user: the user to query
    @type  user: google.appengine.api.users.User
    """
    return models.UserInfo.gql('WHERE user = :1', user).get()


def MakePuzzleTitleForDisplay(p):
    """
    Create a display title for a given puzzle.

    @param p: puzzle
    @type  p: swyzl_models.Puzzle
    """
    pack = models.GetPackForPuzzle(p)
    return '%s, Puzzle %s' % (pack.title, p.name)


class PlayPuzzle(webapp.RequestHandler):
    """Handler for /puzzle/x/y"""

    def get(self, book_index, puzzle_index):
        """
        Handle a GET request.
        
        @param book_index: puzzle book index
        @type  book_index: str
        @param puzzle_index: index of puzzle within book
        @type  puzzle_index: str
        """
        pack = models.GetPack(index=book_index)
        puzzle = models.GetPuzzle(pack_title=pack.title, name=puzzle_index)
        if puzzle:
            title = MakePuzzleTitleForDisplay(puzzle)
            puzzle_viewer.ShowPuzzle(pack.introduction, title, puzzle,
                                     self.request, self.response)
        else:
            self.response.out.write('Puzzle not found!')


class DoneWithPuzzle(webapp.RequestHandler):
    """Handler for /done_with_puzzle"""

    def get(self):
        """
        Handle a GET request. The request is expected to have query parameters

            puzzle_id: index of puzzle being solved
            solution: string containing the user's guess at the puzzle solution

        The response is either "Yes!" if the solution is correct, or
        "Try again." if it is not.
        """
        puzzle_id = self.request.get('puzzle_id')
        user_solution = self.request.get('solution').upper()
        puzzle = db.get(puzzle_id)
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


class NotFound(webapp.RequestHandler):
    """Handler for unofficial URLs"""

    def get(self):
        """Handle a GET request."""
        self.response.out.write("There's nothing to see here. How 'bout a "
                                "<a href='/'>puzzle</a>?")


def WriteTemplate(response, template_name, params, mime_type='text/html'):
    '''
    Fill out a web page template with some parameters and send it as the
    response.
    
    @param response: HTTP response
    @type  response: google.appengine.ext.webapp.Response
    @type  template_name: str
    @param params: parameters for the template
    @type params: dict from string to any kind of object
    @type mime_type: str
    '''
    path = os.path.join(os.path.dirname(__file__), 'templates/%s' %
                        template_name)
    response.headers['Content-Type'] = mime_type
    response.out.write(template.render(path, params))


urls_to_handlers = [('/', MainPage),
                    ('/update', UpdatePacksInMemcacheHandler),
                    ('/about', AboutPage),
                    ('/done_with_puzzle', DoneWithPuzzle),
                    ('/puzzle/(\d+)/(\d+)', PlayPuzzle),
                    ('/tips', TipsPage),
                    ('.*', NotFound)]

application = webapp.WSGIApplication(urls_to_handlers, debug=True)
puzzle_viewer = PuzzleViewer()


def Main():
    """Run the web application."""
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
    Main()
