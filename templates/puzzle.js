
function extractUserSolutionFromTextBoxes() {
  var inputs = document.getElementsByTagName('input');
  var result = [];
  for (var i = 0; i < inputs.length; i++) {
    if (inputs[i].type == 'text') {
      result.push(inputs[i].value);
    }
  }
  return result.join('');
}

/**
 * Makes an Ajax call to verify the solution when user clicks Done button.
 * @param {string} puzzleId BigTable key for the puzzle
 */
function onDone(puzzleId) {
  var userSolution = extractUserSolutionFromTextBoxes();

  var params = "puzzle_id=" + puzzleId +
      "&solution=" + encodeURIComponent(userSolution);
  var myAjax = new Ajax.Request('/done_with_puzzle',
                                {method: 'get',
                                 parameters: params,
                                 onComplete: function(request) {
                                   if (request.responseText == 'Yes!') {
                                     $('alert_div').innerHTML = 'You guessed it!';
                                     setTimeout("goBackToIndex();", 1000);
                                   } else {
                                     // Complain.
                                     $('alert_div').innerHTML = request.responseText;
                                     setTimeout("$('alert_div').innerHTML = '';", 1500);
                                   }
                                 }});
}
