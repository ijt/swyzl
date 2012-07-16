Swyzl: a cryptogram puzzle app on App Engine (swyzl.appspot.com)

Development
===========
To run Python unit tests, do
    
    ./run_tests

To run the application on your local machine, make sure Google AppEngine is
installed and run

    $APP_ENGINE_DIR/dev_appserver.py .
    ./upload_packs_and_puzzles.py

Then point your browser to localhost:8080.

To run Javascript unit tests, point your browser to
    
    ./templates/utils_test.html

