/**
 * JS code that doesn't change for puzzle making.
 */

/**
 * Returns the fields as a dict that will be passed to an ajax call.
 *
 * @param {object} encodingMap A dict from chars to chars
 */
window.getFields = function(encodingMap) {
  var requiredFields = ['message'];
  var missingFields = [];
  for (var i = 0; i < requiredFields.length; i++) {
    var field = requiredFields[i];
    if ($(field).value.length == 0) {
      missingFields.push(field);
    }
  }
  if (missingFields.length > 0) {
    var e = new Error('Missing fields.');
    e.missingFields = missingFields;
    throw e;
  }
  var encodingMapAsString = convertEncodingMapToString(encodingMap);  
  var message = $('message').value;
  var tagsAsString = $('tags').value;
  return {message: encodeURIComponent(message),
          encoding_map: encodingMapAsString,
          short_clue: $('clue_field').value,
          tags: tagsAsString};
}

/**
 * Tries to submit the puzzle, then report problems or go back to main page.
 *
 * @param {Object} encodingMap A map from chars to chars (as strings)
 */
window.onPublish = function(encodingMap) {
  try {
    var params = getFields(encodingMap);
  } catch(e) {
    $('alert').innerHTML = "Can't publish without " + e.missingFields.join(', ') + '.';
    setTimeout("$('alert').innerHTML = '';", 2000);
    return;
  }
  submitNewPuzzle(params);
}

window.submitNewPuzzle = function(params) {
  var myAjax = new Ajax.Request('/submit_new_puzzle',
                                {method: 'get',
                                 parameters: params,
                                 onComplete: function(request) {
                                   if (request.responseText == '') {
                                     goBackToIndex();
                                   } else {
                                     // Complain.
                                     $('alert').innerHTML = request.responseText;
                                     setTimeout("$('alert').innerHTML = '';", 2000)
                                   }
                                 }});
}

window.onSecretMessageKeyUp = function() {
  clearTimeout(swyzl.updateTimer);  // Cancel previously scheduled update.
  swyzl.updateTimer = setTimeout('updatePuzzle()', 1000);
}

/**
 * Updates the puzzle encoding UI from the message box.
 */
window.updatePuzzle = function() {
  var message = $('message').value.toUpperCase();
  new Ajax.Request('/make_puzzle_ui',
                   {method: 'post',
                    parameters: {content: message},
                    onComplete: function(request) {
                      var result = request.responseText.evalJSON();
                      $('cipher_text').innerHTML = result.html + '<hr />';
                      swyzl.encodingMap = result.encodingMap;
                      updateTextBoxesFromEncoding(swyzl.encodingMap);
                    }});
}

window.updateTextBoxesFromEncoding = function(encodingMap) {
  for (var letter in encodingMap) {
    var boxesForThisLetter = $$('input.' + letter);
    var encodedLetter = encodingMap[letter];
    for (var i = 0; i < boxesForThisLetter.length; i++) {
      var box = boxesForThisLetter[i];
      if (box.value != encodedLetter) {
        box.value = encodedLetter;
      }
    }
  }
}

window.highlightConflictingLetters = function(encodingMap) {
  // First figure out which are the conflicting letters.
  var conflictLetters = getConflictLetters(encodingMap);

  // Next, iterate through the text boxes. If the box contains one of the
  // conflicting letters, add the conflict CSS class to it, else remove that
  // class if it's already there.
  var inputs = document.getElementsByTagName('input');
  var result = [];
  for (var i = 0; i < inputs.length; i++) {
    if (inputs[i].type == 'text') {
      if (inputs[i].value in conflictLetters) {
        inputs[i].addClassName('conflict');
      } else {
        inputs[i].removeClassName('conflict');        
      }
    }
  }
}

