import argparse
from lat_epig.parse import scrape

############ UNIT TESTS #################################################################

# Template
# def test_inscription_XXX():
#   # ./parse.py -e 09000264  % --debug
#   args = argparse.Namespace(EDCS='09000264', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')
# 
#   test_output = scrape(args, prevent_write=True, show_inscription_transform=True)
#   assert "[3]" in test_output[0]['inscription']
#   assert "[3]" not in test_output[0]['inscription interpretive cleaning']

def test_language_with_imbalanced_doublequote():
  # ./parse.py -e 78300736  % --debug
  # csvcut -t -c 10,17 output/2021-07-30-EDCS_78300736+term1_%-1.tsv | csvlook
  #  | inscription | language |
  #  | ----------- | -------- |
  #  | "GR         |          |

  args = argparse.Namespace(EDCS='78300736', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')

  test_output = scrape(args, prevent_write=True, show_inscription_transform=True)
  assert '"GR' not in test_output[0]['inscription']
  assert "GR" in test_output[0]['language']


def test_language_with_trailing_imbalanced_doublequote():
  # ./parse.py -e 78800166  % --debug
  # csvcut -t -c 10,17 output/2021-07-30-EDCS_78800166+term1_%-1.tsv | csvlook
  # | inscription | language |
  # | ----------- | -------- |
  # |  // GR"     | PALMYR   |


  args = argparse.Namespace(EDCS='78800166', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')

  test_output = scrape(args, prevent_write=True, show_inscription_transform=True)
  assert 'GR"' not in test_output[0]['inscription']
  assert "PALMYR, GR" in test_output[0]['language']
  
