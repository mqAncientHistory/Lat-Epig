import argparse
from lat_epig.parse import scrape

############ UNIT TESTS #################################################################

######### 1. Cleaning of the text of inscription ########################################
def test_inscription_dubious_dot_subscript():
  # ./parse.py -e 72200182 % --debug
  args = argparse.Namespace(EDCS='76700107', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')

  test_output = scrape(args, prevent_write=True, show_inscription_transform=True)
  assert "ẹ" in test_output[0]['inscription']
  assert "ẹ" not in test_output[0]['inscription interpretive cleaning'] 
  assert "ẹ" not in test_output[0]['inscription conservative cleaning']

def test_inscription_three_both():
  # ./parse.py -e 65300182 % --debug
  args = argparse.Namespace(EDCS='65300182', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')

  test_output = scrape(args, prevent_write=True, show_inscription_transform=True)
  assert "[3]" in test_output[0]['inscription']
  assert "[3]" not in test_output[0]['inscription interpretive cleaning'] 
  assert "[3]" not in test_output[0]['inscription conservative cleaning']

def test_inscription_three_middle():
  # ./parse.py -e 09000264 20700224 % --debug
  args = argparse.Namespace(EDCS='20700224', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')

  test_output = scrape(args, prevent_write=True, show_inscription_transform=True)
  assert "mo[numentum 3 vi]/olaverit" in test_output[0]['inscription']
  assert "mo[numentum 3 vi]/olaverit" not in test_output[0]['inscription conservative cleaning'] 
  assert "mo[numentum 3 vi]/olaverit" not in test_output[0]['inscription interpretive cleaning']

def test_inscription_six():
  # ./parse.py -e 31900104  % --debug
  args = argparse.Namespace(EDCS='31900104', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')

  test_output = scrape(args, prevent_write=True, show_inscription_transform=True)
  assert "[6]" in test_output[0]['inscription']
  assert "[6]" not in test_output[0]['inscription interpretive cleaning']
  assert "[6]" not in test_output[0]['inscription conservative cleaning']


def test_inscription_one():
  # ./parse.py -e 10400149  % --debug
  args = argparse.Namespace(EDCS='10400149', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')

  test_output = scrape(args, prevent_write=True, show_inscription_transform=True)
  assert "[1]" in test_output[0]['inscription']
  assert "[1]" not in test_output[0]['inscription interpretive cleaning']
  assert "[1]" not in test_output[0]['inscription conservative cleaning']


### EXTRA QUOTES - find better example inscription
#def test_inscription_quotes():
#  # ./parse.py -e 10501222  % --debug
#  args = argparse.Namespace(EDCS='10501222', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')

#  test_output = scrape(args, prevent_write=True, show_inscription_transform=True)
#  assert "[\u0022]" in test_output[0]['inscription']
#  assert "[\u0022]" not in test_output[0]['inscription interpretive cleaning']
#  assert "[\u0022]" not in test_output[0]['inscription conservative cleaning']

### EXTRA BACKSLASH - find better example inscription
#def test_inscription_quotes():
#  # ./parse.py -e 10501222  % --debug
#  args = argparse.Namespace(EDCS='10501222', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')

#  test_output = scrape(args, prevent_write=True, show_inscription_transform=True)
#  assert "[\u005C]" in test_output[0]['inscription']
#  assert "[\u005C]" not in test_output[0]['inscription interpretive cleaning']
#  assert "[\u005C]" not in test_output[0]['inscription conservative cleaning']


def test_inscription_expanded_abbreviations():
  # ./parse.py -e 27000432  % --debug
  args = argparse.Namespace(EDCS='27000432', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')

  test_output = scrape(args, prevent_write=True, show_inscription_transform=True)
  assert "D(is) M(anibus)" in test_output[0]['inscription']
  assert "D(is) M(anibus)" not in test_output[0]['inscription conservative cleaning']
  assert "D M " in test_output[0]['inscription conservative cleaning']
  assert "Dis Manibus" in test_output[0]['inscription interpretive cleaning']


def test_inscription_suppresion():
  # ./parse.py -e 27800893  % --debug
  args = argparse.Namespace(EDCS='27800893', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')

  test_output = scrape(args, prevent_write=True, show_inscription_transform=True)
  assert "praetoria{e}" in test_output[0]['inscription']
  assert "praetoria{e}" not in test_output[0]['inscription conservative cleaning']
  assert "praetoriae " in test_output[0]['inscription conservative cleaning']
  assert "praetoria" in test_output[0]['inscription interpretive cleaning']


def test_inscription_restoration():
  # ./parse.py -e 34100092  % --debug
  args = argparse.Namespace(EDCS='34100092', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')

  test_output = scrape(args, prevent_write=True, show_inscription_transform=True)
  assert "nillae c[oniugi]" in test_output[0]['inscription']
  assert "nillae c[oniugi]" not in test_output[0]['inscription conservative cleaning']
  assert "nillae c " in test_output[0]['inscription conservative cleaning']
  assert "nillae coniugi" in test_output[0]['inscription interpretive cleaning']

def test_inscription_substitution_edh():
  
  # ./parse.py -e 63600442 % --debug
  args = argparse.Namespace(EDCS='63600442', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')
  test_output = scrape(args, prevent_write=True, show_inscription_transform=True)

  assert "<F=P>urius" in test_output[0]['inscription']
  assert "Purius" in test_output[0]['inscription conservative cleaning'] 
  assert "Furius" in test_output[0]['inscription interpretive cleaning'] 


def test_inscription_substitution():
  # ./parse.py -e 34100092  % --debug
  args = argparse.Namespace(EDCS='15300609', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')

  test_output = scrape(args, prevent_write=True, show_inscription_transform=True)
  assert "sanc<t=I>issi<ma=AM>" in test_output[0]['inscription']
  assert "sanc<t=I>issi<ma=AM>" not in test_output[0]['inscription conservative cleaning']
  assert "sanc<t=I>issi<ma=AM>" not in test_output[0]['inscription interpretive cleaning']

def test_inscription_que():
  # ./parse.py -e 54601011  % --debug
  args = argparse.Namespace(EDCS='54601011', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')

  test_output = scrape(args, prevent_write=True, show_inscription_transform=True)
  assert "libertabusque" in test_output[0]['inscription']
  assert "libertabusque" not in test_output[0]['inscription conservative cleaning']
  assert "libertabusque" not in test_output[0]['inscription interpretive cleaning']
  assert "libertabus que " in test_output[0]['inscription conservative cleaning']
  assert "libertabus que " in test_output[0]['inscription interpretive cleaning']

def test_inscription_vir():
  # ./parse.py -e 24900101  % --debug
  args = argparse.Namespace(EDCS='24900101', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')

  test_output = scrape(args, prevent_write=True, show_inscription_transform=True)
  assert "IIIIvir" in test_output[0]['inscription']
  assert "IIIIvir" not in test_output[0]['inscription conservative cleaning']
  assert "IIIIvir" not in test_output[0]['inscription interpretive cleaning']
  assert "IIII vir " in test_output[0]['inscription conservative cleaning']
  assert "IIII vir " in test_output[0]['inscription interpretive cleaning']

# Template
#def test_inscription_XXX():
#  # ./parse.py -e 09000264  % --debug
#  args = argparse.Namespace(EDCS='09000264', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')
#
#  test_output = scrape(args, prevent_write=True, show_inscription_transform=True)
#  assert "[3]" in test_output[0]['inscription']
#  assert "[3]" not in test_output[0]['inscription interpretive cleaning']

