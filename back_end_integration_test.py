"""To run this test case, go to the App Engine admin console and paste these
lines:

import back_end_integration_test
back_end_integration_test.run()

"""


def testMainPageGetUserInfo():
  main_page_handler = main_view.MainPage()


def IsTestFunction(x):
  """Tells whether a given object is a test function."""
  return isinstance(x, type(lambda y: None)) and (
      x.__name__.startswith('test') or
      x.__name__.contains('Should'))


def GetTestFunctions():
  """Gets all the test functions in this file."""
  this_module = __import__(__name__)
  return [f for f in this_module.__dict__.values() if IsTestFunction(f)]
  

def run():
  """Runs the integration tests."""
  test_functions = GetTestFunctions()
  for f in test_functions:
    f()
  print 'Successfully ran %s tests' % len(test_functions)

