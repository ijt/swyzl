var BACKSPACE = 8;
var IPHONE_BACKSPACE = 127;
var SPACE = 32;
var SHIFT_TAB = 16;
var LEFT_ARROW = 37;
var RIGHT_ARROW = 39;
var TAB = 9;

/**
 * Returns the base url.
 *
 * @param loc: window.location
 */
function getBaseUrl(loc) {
  var baseUrl = 'http://' + loc.hostname;
  if (loc.port) {
    baseUrl = baseUrl + ':' + loc.port; 
  }
  return baseUrl;
}

function goBackToIndex() {
  window.location = getBaseUrl(window.location);
}

function isLetterCode(code) {
  return (code >= 'a'.charCodeAt(0) &&
          code <= 'z'.charCodeAt(0)) ||
         (code >= 'A'.charCodeAt(0) &&
          code <= 'Z'.charCodeAt(0));
}

function isLetter(s) {
  return (s.length != 1) ? false : isLetterCode(s.charCodeAt(0));
}

/**
 * Updates other text boxes with the same cipher char as the one typed into.
 */
function onKeyDown(cipherChar, userCharCode, currentBoxIndex) {
  // Get all the boxes having a class equal to the cipher char.
  var boxes = $$('input.' + cipherChar);
  var userChar;
  if (userCharCode == BACKSPACE || userCharCode == IPHONE_BACKSPACE) {
    userChar = ' ';
  } else if (userCharCode == SHIFT_TAB || userCharCode == TAB) {
    return true;
  } else {
    userChar = String.fromCharCode(userCharCode).toUpperCase();
  }

  // Update all text boxes that have the same cipher char.
  if (isLetterCode(userCharCode) || userChar == ' ') {
    for (var i = 0; i < boxes.length; i++) {
      var box = boxes[i];
      box.value = userChar;
    }
  }

  var boxToFocus = null;

  // Move to the next text box if the key was spacebar or a letter or right
  // arrow.
  if (isLetterCode(userCharCode) || userCharCode == SPACE ||
      userCharCode == RIGHT_ARROW) {
    var boxToFocus = $('box' + (currentBoxIndex + 1))
  }
  
  // Move back on backspace or left arrow.
  if (userCharCode == BACKSPACE || userCharCode == LEFT_ARROW) {
    var boxToFocus = $('box' + (currentBoxIndex - 1))
  }
  
  if (boxToFocus) {
    boxToFocus.focus();
  }

  // Return false to prevent lowercase letters or punctuation from getting in.
  return false;
}

/**
 * Converts maps like {'A':'B', 'Z':'X'} to strings like 'ABZX'.
 */
function convertEncodingMapToString(map) {
  var encodingMapParts = [];
  for (var fromLetter in map) {
    encodingMapParts.push(fromLetter);
    encodingMapParts.push(map[fromLetter]);
  }
  return encodingMapParts.join('');
}

function isAlphaCode(code) {
  return (('a'.charCodeAt(0) <= code && code <= 'z'.charCodeAt(0))
       || ('A'.charCodeAt(0) <= code && code <= 'Z'.charCodeAt(0)));
}

/**
 * Gets all links that aren't JavaScript or mailto.
 */
function getNonJavaScriptLinks() {
  var result = [];
  var links = document.getElementsByTagName('a');
  for (var i = 0; i < links.length; i++) {
    var href = links[i].href;
    if (!href.match(/^javascript:/) && !href.match(/^mailto:/)) {
      result.push(links[i]);
    }
  }
  return result;
}

/**
 * Returns true if two lists (arrays) have identical elements.
 */
function listsEqual(a, b) {
  if (a.length != b.length) {
    return false;
  }
  for (var i = 0; i < a.length; i++) {
    if (a[i] != b[i]) {
      return false;
    }
  }
  return true;
}

/**
 * Returns the letters in conflict.
 */
function getConflictLetters(encodingMap) {
  var result = {};
  var histo = {};
  for (var x in encodingMap) {
    var y = encodingMap[x];
    histo[y] = (histo[y] || 0) + 1;
    if (histo[y] >= 2) {
      result[y] = true;
    }
  }
  return result;
}
