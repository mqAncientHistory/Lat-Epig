import argparse
from lat_epig.parse import scrape




############ 2. Date parsing ##############################################################

def test_no_letters_at_all():
  #  'raw dating': '163 to 170;  163 to 163',
  # ./parse.py -e 01000244 % --debug
  args = argparse.Namespace(EDCS='01000244', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')
  test_output = scrape(args, prevent_write=True)

  assert test_output[0]['dating from'] == 163
  assert test_output[0]['dating to'] == 170
  assert test_output[0]['date not before'] == 163
  assert test_output[0]['date not after'] == 170

def test_no_letter():
  #  'raw dating': 'b:  96 to 96;  81 to 96',
  args = argparse.Namespace(EDCS='72300077', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')
  
  test_output = scrape(args, prevent_write=True)
  
  assert test_output[0]['dating from'] == 96
  assert test_output[0]['dating to'] == 96
  assert test_output[0]['date not before'] == 81
  assert test_output[0]['date not after'] == 96

def test_a_k_dates():
  # dating:  a:  196 to 196;   b:  198 to 200;   c:  171 to 300;   d:  208 to 218;   e:  180 to 222;   f:  228 to 228;   g:  234 to 234;   h:  297 to 297;   i:  171 to 300;   j:  171 to 300;   k:  171 to 300         
  # EDCS-ID: EDCS-72200182 
  args = argparse.Namespace(EDCS='72200182', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')
  test_output = scrape(args, prevent_write=True)

  assert test_output[0]['dating from'] == 196
  assert test_output[0]['dating to'] == 196
  assert test_output[0]['date not before'] == 171
  assert test_output[0]['date not after'] == 300

def test_digit_colon():
  #  digit with colon 3:  ;  -27 to 37
  #  EDCS-75100087 
  args = argparse.Namespace(EDCS='75100087', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')

  test_output = scrape(args, prevent_write=True)

  assert test_output[0]['dating from'] == -27
  assert test_output[0]['dating to'] == 37
  assert test_output[0]['date not before'] == -27
  assert test_output[0]['date not after'] == 37

def test_digit_colon_empty():
  #  digit with colon 1:
  #  EDCS-74200019 
  args = argparse.Namespace(EDCS='74200019', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')

  test_output = scrape(args, prevent_write=True)

  assert test_output[0]['dating from'] == None
  assert test_output[0]['dating to'] == None
  assert test_output[0]['date not before'] == None
  assert test_output[0]['date not after'] == None

def test_single_date():
  #  dating: -20         
  #  EDCS-ID: EDCS-41200809

  args = argparse.Namespace(EDCS='41200809', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')

  test_output = scrape(args, prevent_write=True)

  assert test_output[0]['dating from'] == -20
  assert test_output[0]['dating to'] == -20
  assert test_output[0]['date not before'] == -20
  assert test_output[0]['date not after'] == -20

def test_single_valued_datespan():
  # dating: -68 to -68                  
  #  EDCS-ID: EDCS-24900077

  args = argparse.Namespace(EDCS='24900077', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')

  test_output = scrape(args, prevent_write=True)

  assert test_output[0]['dating from'] == -68
  assert test_output[0]['dating to'] == -68
  assert test_output[0]['date not before'] == -68
  assert test_output[0]['date not after'] == -68


def test_missing_first_date():
  # dating:  to 100                  
  #  EDCS-ID: EDCS-34901010

  args = argparse.Namespace(EDCS='34901010', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')

  test_output = scrape(args, prevent_write=True)

  assert test_output[0]['dating from'] == None
  assert test_output[0]['dating to'] == 100
  assert test_output[0]['date not before'] == None
  assert test_output[0]['date not after'] == 100


def test_random__middle_date():
  # # dating:  a:  ;   b:  71 to 100;   c:  ;   d:                             
  #  EDCS-ID: EDCS-32001032

  args = argparse.Namespace(EDCS='32001032', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')

  test_output = scrape(args, prevent_write=True)

  assert test_output[0]['dating from'] == 71
  assert test_output[0]['dating to'] == 100
  assert test_output[0]['date not before'] == 71
  assert test_output[0]['date not after'] == 100

############ End of UNIT TESTS ##############################################################
