import argparse
from lat_epig.parse import scrape
import re
############ UNIT TESTS #################################################################

# Template
# def test_inscription_XXX():
#   # ./parse.py -e 09000264  % --debug
#   args = argparse.Namespace(EDCS='09000264', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')
# 
#   test_output = scrape(args, prevent_write=True, show_inscription_transform=True)
#   assert "[3]" in test_output[0]['inscription']
#   assert "[3]" not in test_output[0]['inscription interpretive cleaning']

def test_EDCS_ID():
  # ./parse.py -e EDCS-07600345  % --debug
 
  args = argparse.Namespace(EDCS='07600345', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')

  test_output = scrape(args, prevent_write=True, show_inscription_transform=True)
  assert "[]" not in test_output[0]['EDCS-ID']
  assert re.match(r"EDCS-[0-9]{8,8}", test_output[0]['EDCS-ID'])


def test_publication():
  # ./parse.py -e 78800166  % --debug

  args = argparse.Namespace(EDCS='78800166', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')

  test_output = scrape(args, prevent_write=True, show_inscription_transform=True)
  assert "AE 1937, 00075" in test_output[0]['publication']
  assert "[]" not in test_output[0]['publication']

def test_province():
  # ./parse.py -e 78800170  % --debug

  args = argparse.Namespace(EDCS='78800170', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')

  test_output = scrape(args, prevent_write=True, show_inscription_transform=True)
  assert "Pontus et Bithynia" in test_output[0]['province']
  assert "Pontus et Bithynia" not in test_output[0]['place']
  assert "[]" not in test_output[0]['province']


def test_place():
  # ./parse.py -e 16201127  % --debug

  args = argparse.Namespace(EDCS='16201127', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')

  test_output = scrape(args, prevent_write=True, show_inscription_transform=True)
  assert '[]' not in test_output[0]['place']
  assert "Acireale / Acium" in test_output[0]['place']

def test_status():
  # ./parse.py -e 55701594  % --debug

  args = argparse.Namespace(EDCS='55701594', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')

  test_output = scrape(args, prevent_write=True, show_inscription_transform=True)
  assert '[]' not in test_output[0]['status']
  assert "sigilla impressa;  tituli fabricationis" in test_output[0]['status']

def test_material():
  # ./parse.py -e 32001159  % --debug

  args = argparse.Namespace(EDCS='32001159', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')

  test_output = scrape(args, prevent_write=True, show_inscription_transform=True)
  assert '[]' not in test_output[0]['Material']
  assert "lapis" in test_output[0]['Material']

def test_comment():
  # ./parse.py -e 36400015  % --debug

  args = argparse.Namespace(EDCS='36400015', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')

  test_output = scrape(args, prevent_write=True, show_inscription_transform=True)
  assert "comment DOI: 10.3406/crai.2005.22934" not in test_output[0]['inscription']
  assert "comment DOI: 10.3406/crai.2005.22934" in test_output[0]['Comment']


# Petra continue from here

# def test_latitude():
#   # ./parse.py -e 78800166  % --debug
#   # csvcut -t -c 10,17 output/2021-07-30-EDCS_78800166+term1_%-1.tsv | csvlook
#   # | inscription | language |
#   # | ----------- | -------- |
#   # |  // GR"     | PALMYR   |


#   args = argparse.Namespace(EDCS='78800166', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')

#   test_output = scrape(args, prevent_write=True, show_inscription_transform=True)
#   assert 'GR"' not in test_output[0]['inscription']
#   assert "PALMYR, GR" in test_output[0]['language']

# def test_longitude():
#   # ./parse.py -e 78800166  % --debug
#   # csvcut -t -c 10,17 output/2021-07-30-EDCS_78800166+term1_%-1.tsv | csvlook
#   # | inscription | language |
#   # | ----------- | -------- |
#   # |  // GR"     | PALMYR   |


#   args = argparse.Namespace(EDCS='78800166', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')

#   test_output = scrape(args, prevent_write=True, show_inscription_transform=True)
#   assert 'GR"' not in test_output[0]['inscription']
#   assert "PALMYR, GR" in test_output[0]['language']

# def test_photo():
#   # ./parse.py -e 78800166  % --debug
#   # csvcut -t -c 10,17 output/2021-07-30-EDCS_78800166+term1_%-1.tsv | csvlook
#   # | inscription | language |
#   # | ----------- | -------- |
#   # |  // GR"     | PALMYR   |


#   args = argparse.Namespace(EDCS='78800166', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')

#   test_output = scrape(args, prevent_write=True, show_inscription_transform=True)
#   assert 'GR"' not in test_output[0]['inscription']
#   assert "PALMYR, GR" in test_output[0]['language']

# def test_partner_link():
#   # ./parse.py -e 78800166  % --debug
#   # csvcut -t -c 10,17 output/2021-07-30-EDCS_78800166+term1_%-1.tsv | csvlook
#   # | inscription | language |
#   # | ----------- | -------- |
#   # |  // GR"     | PALMYR   |


#   args = argparse.Namespace(EDCS='78800166', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')

#   test_output = scrape(args, prevent_write=True, show_inscription_transform=True)
#   assert 'GR"' not in test_output[0]['inscription']
#   assert "PALMYR, GR" in test_output[0]['language']

# def test_extra_text():
#   # ./parse.py -e 78800166  % --debug
#   # csvcut -t -c 10,17 output/2021-07-30-EDCS_78800166+term1_%-1.tsv | csvlook
#   # | inscription | language |
#   # | ----------- | -------- |
#   # |  // GR"     | PALMYR   |


#   args = argparse.Namespace(EDCS='78800166', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')

#   test_output = scrape(args, prevent_write=True, show_inscription_transform=True)
#   assert 'GR"' not in test_output[0]['inscription']
#   assert "PALMYR, GR" in test_output[0]['language']

# def test_extra_html():
#   # ./parse.py -e 78800166  % --debug
#   # csvcut -t -c 10,17 output/2021-07-30-EDCS_78800166+term1_%-1.tsv | csvlook
#   # | inscription | language |
#   # | ----------- | -------- |
#   # |  // GR"     | PALMYR   |


#   args = argparse.Namespace(EDCS='78800166', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')

#   test_output = scrape(args, prevent_write=True, show_inscription_transform=True)
#   assert 'GR"' not in test_output[0]['inscription']
#   assert "PALMYR, GR" in test_output[0]['language']
