# In the interactive console, type
#
# import data.parks1
# data.parks1.Save()
#
# if these puzzles are not already in the data store.
#

import models

def Save():
  intro = ('In these cryptograms, each letter represents another '
      'consistently throughout '
      'the puzzle.  Substitute by trial and error to reveal a message about a State or National '
      'Park.  As hints, the puzzle includes the two letter postal code of the state '
      'containing the park, and another word hint.  '
      'Below the puzzle is an alphabet area to keep track of what the letters represent '
      'while you figure them out.')

  parks_pack = models.PackOfPuzzles(
      title="Park Puzzlers - Volume One",
      introduction = intro,
      puzzle_keys=[],
      price_cents=100,
      thumbnail_url_part='parks-1.jpg')

  data = [
      ("EA XCB, VSA, CM MQEA GCS WQA HCCZ XCM QBQNLV CA NPL DLQWP QAT DQAQAQ VHSBV EA NPL XCMLVN QAG TQG QN OQNMEWZ'V OCEAN ALQM NMEAETQT, WQHEXCMAEQ.",
       "IN FOG, SUN, OR RAIN YOU CAN LOOK FOR AGATES ON THE BEACH AND BANANA SLUGS IN THE FOREST ANY DAY AT PATRICK'S POINT NEAR TRINIDAD, CALIFORNIA.",
       "D is B", '1', "Ocean"),
      ("GYS GMWSK BFZS ME VEW FOG FZSC GMWS HFFQK, CMNY JMGY KSV QMXS, JYMQS HSFHQS, CMNY JMGY QMXS, BFZS JMGYFOG BFGFCK VQFED NVCCMVDS CFVWK VG VNVWMV, BVMES.",
       "THE TIDES MOVE IN AND OUT OVER TIDE POOLS, RICH WITH SEA LIFE, WHILE PEOPLE, RICH WITH LIFE, MOVE WITHOUT MOTORS ALONG CARRIAGE ROADS AT ACADIA, MAINE.",
       "D is G", '2', "Fog"),
      ("NO VUR LUZFAM AK VUR \"UNTU AOR\" (BAPOV BYQNOERC) UPTR YZJNXAP ZOF BNONZVPJR MNEFKEAMRJL LUZJR UZXNVZV NO FROZEN, ZEZLQZ.",
       "IN THE SHADOW OF THE \"HIGH ONE\" (MOUNT MCKINLEY) HUGE CARIBOU AND MINIATURE WILDFLOWERS SHARE HABITAT IN DENALI, ALASKA.",
       "K is F", '3', "Frozen"),
      ("DVIX QVXYSOOSLD, BLACK HIELCI MLA FID ZLOOLJ CKV CXISO LZ OVJSB IDH FOIXE SD BWSXSC YLADH KSBCLXSF WXISXSV JKVXV CKVM QSVJVH I UVIACSZAO OIDHBFIWV IDH KVXHB LZ UAZZIOL.",
       "NEAR VERMILLION, SOUTH DAKOTA YOU CAN FOLLOW THE TRAIL OF LEWIS AND CLARK IN SPIRIT MOUND HISTORIC PRAIRIE WHERE THEY VIEWED A BEAUTIFUL LANDSCAPE AND HERDS OF BUFFALO.",
       "Q is V", '4', "Black"),
      ("RDMGV CROC OKG HWA FL OMMXAOCDKV ZKDJXHG VWKJXJOM BDK BXVR, CWKCMGV, OQH VQOXMV HWKXQA CRG HKL VGOVDQ; OQH XFXV OQH EDDH VCDKYV OKG CED DB CRG YXQHV DB FXKHV CROC ZDZWMOCG CRG BMDKXHO GJGKAMOHGV.",
       "HOLES THAT ARE DUG BY ALLIGATORS PROVIDE SURVIVAL FOR FISH, TURTLES, AND SNAILS DURING THE DRY SEASON; AND IBIS AND WOOD STORKS ARE TWO OF THE KINDS OF BIRDS THAT POPULATE THE FLORIDA EVERGLADES.",
       "Z is P", '5', "Croc"),
      # More here...
    ]

  for row in data:
    puzzle = models.Puzzle(cipher_text=row[0], solution_text=row[1], short_clue=row[2],
                           name=row[3])
    puzzle.put()
    parks_pack.puzzle_keys.append(puzzle.key())

  parks_pack.put()

