import models

space = models.PuzzleBook(
    name="Crypto Riddles - Outer Space",
    short_name='space',
    intro = 'In these cryptograms, each letter represents another '
        'consistently throughout '
        'the puzzle.  Substitute by trial and error to reveal a question and answer about '
        'something of interest relating to outer space.  Each question begins with "who", '
        '"what", "when" or "why."  A letter clue is given and a word hint is shown.  '
        'Below the puzzle is an alphabet area to keep track of what the letters represent '
        'while you figure them out.')
space.put()

r = models.Riddle(index=1,
    cipher_question=  'EQH EJD WQO JDWFHKHYOF IHF EQHY J WOCODSHAO ND KJYOZ WQJW QJD LOOK HFLNWNKX WQO OJFWQ HRWDNZO WQO JWYHDAQOFO, WJVNKX JKZ DOKZNKX LJSV IJKWJDWNS AQHWHXFJAQD?',
    solution_question='WHO WAS THE ASTRONOMER FOR WHOM A TELESCOPE IS NAMED THAT HAS BEEN ORBITING THE EARTH OUTSIDE THE ATMOSPHERE, TAKING AND SENDING BACK FANTASTIC PHOTOGRAPHS?',
    cipher_answer=  'OZENK QRLLCO',
    solution_answer='EDWIN HUBBLE',
    clue_word='LOOK',
    clue='V is K',
    book_short_name='space')
r.put()

r = models.Riddle(index=2,
    cipher_question=  'GEXO LC OEA KXYWI IJ OEA CESOOHA GEAR LO WIAC OI OEA LROAYRXOLIRXH CZXKA COXOLIR?',
    solution_question='WHAT IS THE CARGO OF THE SHUTTLE WHEN IT GOES TO THE INTERNATIONAL SPACE STATION?',
    cipher_answer=  'JIIQ, JSAH XRQ CSZZHLAC',
    solution_answer='FOOD, FUEL AND SUPPLIES',
    clue_word='GEAR',
    clue='K is C',
    book_short_name='space')
r.put()