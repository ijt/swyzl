/**
 * Code that runs each time the Make Your Own tab is clicked.
 */

swyzl.potentialEncodingMap = {{ initial_encoding_map }};
swyzl.encodingMap = {};
swyzl.updateTimer = null;


// Set up Scriptaculous autocomplete.
swyzl.tags = {{ tags }};

new Autocompleter.Local('tags', 'tag_list', swyzl.tags,
    {'fullSearch': true,
     'tokens': [',']});

// FIXME: We should be setting onKeyDown back to its original value after leaving
// the Make Your Own tab.
var savedOnKeyDown = onKeyDown;  // Defined in utils.js.
window.onKeyDown = function(labelLetter, boxLetterCode) {
  var boxLetter = String.fromCharCode(boxLetterCode);
  if (isAlphaCode(boxLetterCode)) {
     swyzl.encodingMap[labelLetter] = boxLetter;
  }
  savedOnKeyDown(labelLetter, boxLetterCode);
  highlightConflictingLetters(swyzl.encodingMap);
}

