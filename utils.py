"""Misc helper functions that do not depend on App Engine"""

import random


def MakeRandomLetterMap():
    """
    Make a one-to-one map from every capital letter to every other.
    
    @return: a mapping with a random permutation of letters
    @rtype: dict
    """
    alphabet = [chr(c) for c in range(ord('A'), ord('Z') + 1)]
    shuffled = alphabet[:]
    random.shuffle(shuffled)
    return dict((alphabet[i], shuffled[i]) for i in xrange(len(alphabet)))


def GetLetters(string):
    """Get the set of letters in a given string."""
    return set([x for x in string.upper() if x.isalpha()])


def MakeRandomLetterMapForLettersIn(message):
    """Make a map from letters in a message to other letters.
    
    @param message: text to use as the domain for the map
    @type  message: str
    @return: map from the message letters to randomly chosen other letters
    """
    letters = GetLetters(message)
    bigmap = MakeRandomLetterMap()
    return dict((l, bigmap[l]) for l in letters)


def MakeEncryptionMap(solution_text, cipher_text):
    """Makes an encryption map from a solution and cipher."""
    if len(solution_text) != len(cipher_text):
        raise ValueError('Solution and cipher lengths do not match')
    result = {}
    for i in    xrange(len(solution_text)):
        s = solution_text[i]
        c = cipher_text[i]
        if result.has_key(s):
            if result[s] != c:
                raise ValueError('Character %s maps to both %s and %s.' %
                                                 (s, result[s], c))
        else:
            if s.isalpha():
                result[s] = c
            else:
                if s != c:
                    raise ValueError("Non-letter %s mapped to %s. That's not allowed." %
                                                     (s, c))
    return result


def CheckPuzzle(solution_text, cipher_text):
    """Makes sure that the solution and cipher imply a 1-1 map."""
    MakeEncryptionMap(solution_text, cipher_text)
    MakeEncryptionMap(cipher_text, solution_text)


def ConvertStringToEncodingMap(string):
    """Converts strings like 'ABZX' to maps like {'A':'B', 'Z':'X'}."""
    n = len(string) / 2
    evens = [string[2 * i] for i in xrange(n)]
    odds = [string[2 * i + 1] for i in xrange(n)]
    return dict((evens[i], odds[i]) for i in xrange(n))


def ListToTableRow(lst, klass=None):
    class_part = klass and (' class="%s"' % klass) or ''
    td = '<td%s>' % class_part
    inner_part = ('</td>%s' % td).join(lst)
    return '<tr>' + td + inner_part + '</td></tr>'


def GenerateWordHtmls(cipher_words):
    """Generates a list of html snippets to build a puzzle UI."""
    word_htmls = []

    # Generate one table per word.
    box_index = 0
    for word in cipher_words:
        top_row = []
        bot_row = []
        for char in word:
            if char.isalpha():
                # The code char is part of the input tag's class.    That way we can
                # easily find all the input boxes for a given code character.
                input_tag = ('<input id="box%s" class="SwyzlTextBox %s" maxlength="1" '
                                         % (box_index, char))
                # The size is set to 2 because setting it to 1 is supposed to not be
                # well supported on all browsers.    The onKeyPress callback is defined
                # in the GWT code.
                callback = ("return onKeyDown('%s', event.keyCode || event.which, %i)" %
                                        (char, box_index))
                input_tag += 'size="2" onkeyDown="%s">' % callback
                top_row.append(input_tag)
                bot_row.append(char)
                box_index += 1
            else:
                # Use the same CSS class as the text boxes to keep things lined up.
                elt = '<span class="SwyzlTextBox noborder">%s</span>' % char
                top_row.append(elt)
                bot_row.append(elt)
        word_html = '<table class="boxOnLetter">'
        word_html += ListToTableRow(top_row)
        word_html += ListToTableRow(bot_row, klass="letter")
        word_html += '</table>'
        word_htmls.append(word_html)
    return word_htmls


def GenerateAlphabetUi():
    """Constucts HTML for the alphabet UI to keep track of mapped letters."""
    html_lists = [GenerateWordHtmls(chr(x)) for x in range(ord('A'), ord('Z') + 1)]
    htmls = [html for [html] in html_lists]
    return '<div id="alphabet_div">%s</div>' % '\n'.join(htmls)

