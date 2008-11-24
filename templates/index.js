function setContentTo(url) {
  new Ajax.Request(url,
                   {method: 'get',
                    parameters: {},
                    onComplete: function(request) {
                      $('content').innerHTML = request.responseText;
                      makeAllLinksDoAjaxCallsAndPutTheResultsIntoTheContentDiv();
                    }});
  setActiveTab(null);
}

function init() {
  playPuzzleOfTheDay();
}

function getTabs() {
  var tabIds = ['tab-make', 'tab-play', 'tab-tips'];
  var result = [];
  for (var i = 0; i < tabIds.length; i++) {
    result.push($(tabIds[i]));
  }
  return result;
}

function setActiveTab(tabId) {
  var tabs = getTabs();
  for (var i = 0; i < tabs.length; i++) {
    var tab = tabs[i];
    if (tab) {
      var klass = tab.id == tabId ? 'active' : '';
      if (tab.id == tabId) {
        tab.addClassName('active');
      } else {
        tab.removeClassName('active');
      }
    }
  }
}

function playPuzzleOfTheDay() {
  setContentTo("/potd");
  setActiveTab('tab-play');
}

function makePuzzle() {
  setContentTo("/make");
  runJsAtUrl("/js_for_make");
  setActiveTab('tab-make');
}

function tips() {
  setContentTo("/tips");
  setActiveTab('tab-tips');
}

/**
 * Fetches some JavaScript from an URL with an Ajax call and then runs it.
 * @param {string} url
 */
function runJsAtUrl(url) {
  new Ajax.Request(url,
                   {method: 'get',
                    parameters: {},
                    onComplete: function(request) {
                      eval(request.responseText);
                    }});
}




