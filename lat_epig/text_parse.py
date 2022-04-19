from pprint import pprint
import re


def clean_conservative_rules():
  rules = {"inscription_dubious_dot_subscript": {"patt":re.compile(r'\u0323', re.UNICODE),
                      "replace":r""},
        "inscription_edcs_number_three_both": {"patt":re.compile(r'\[3\]', re.UNICODE),
                      "replace":r"[-] "},
        "inscription_edcs_number_three_right": {"patt":re.compile(r'3\]', re.UNICODE),
                      "replace":r"-] "},
        "inscription_edcs_number_three_left": {"patt":re.compile(r'\[3', re.UNICODE),
                      "replace":r" [-"},
        "inscription_edcs_number_three_middle": {"patt":re.compile(r'(\[\w+)( [3] )(\w+\])', re.UNICODE),
                      "replace":r" \1 \3 "},
        "inscription_edcs_number_six_both": {"patt":re.compile(r'\[6\]', re.UNICODE),
                      "replace":r"[-] "},
        "inscription_edcs_number_one": {"patt":re.compile(r'[1]', re.UNICODE),
                      "replace":r" "},
        "inscription_edcs_quotes": {"patt":re.compile(r'\u0022', re.UNICODE),
                      "replace":r" "},
        "inscription_edcs_backslashes": {"patt":re.compile(r'\u005C\u005C', re.UNICODE),
                      "replace":r" "},
        "inscription_expanded_abbreviations_conservative": {"patt":re.compile(r'\([^(]*\)', re.UNICODE),
                      "replace":r""},
        "inscription_suppresion_superscripts_conservative": {"patt":re.compile(r'{[^}]*}[⁰¹²³⁴⁵⁶⁷⁸⁹]+', re.UNICODE),
                                   "replace":r""},
        "inscription_suppresion_conservative": {"patt":re.compile(r'[\{*\}]', re.UNICODE),
                                   "replace":r""},
        "inscription_restoration_conservative": {"patt":re.compile(r'\[[^[]*\]', re.UNICODE),
                                   "replace":r""},
        "inscription_substitution_edh_conservative": {"patt":re.compile(r'(\<)([α-ωΑ-Ωa-zA-Z])=([α-ωΑ-Ωa-zA-Z])(\>)', re.UNICODE),
                                   "replace":r"\3"},
         "inscription_substitution_edh_conservative_missing": {"patt":re.compile(r'(\<)([α-ωΑ-Ωa-zA-Z])*=([α-ωΑ-Ωa-zA-Z])(\>)', re.UNICODE),
                                   "replace":r"\3"},                          
        "inscription_substitution_conservative": {"patt":re.compile(r'\<[^<]*\>', re.UNICODE),
                                   "replace":r""},
        "inscription_new_line": {"patt":re.compile(r'[\||\/|\/\/]', re.UNICODE),
                      "replace":r""},
        "inscription_interpunction_symbols": {"patt":re.compile(r'[=\+\,|\.|․|:|⋮|⁙|;|!|\-|—|–|#|%|\^|&|\~|@]', re.UNICODE),
                      "replace":r" "},
        "inscription_epigraphic_symbols": {"patt":re.compile(r'[❦|·|∙|𐆖|⏑|⏓|⏕]', re.UNICODE),
                      "replace":r""},
        "inscription_uncertainty_symbols": {"patt":re.compile(r'[\\?]', re.UNICODE),
                      "replace":r""},
        "inscription_arabic_numerals": {"patt":re.compile(r'[0-9]+', re.UNICODE),
                      "replace":r""},
        "inscription_unclosed_brackets": {"patt":re.compile(r'[\[|\{|\(|\)|\}|\]]', re.UNICODE),
                      "replace":r""},
        "inscription_edcs_que": {"patt":re.compile(r'(\w+)(que)\b', re.UNICODE),
                      "replace":r"\1 \2"},
        "inscription_edcs_vir": {"patt":re.compile(r'([I|V|X])(vir*)', re.UNICODE),
                      "replace":r"\1 \2"},
        "inscription_extra_blank": {"patt":re.compile(r'[ ]+', re.UNICODE),
                      "replace":r" "},
        "inscription_multi_whitespace": {"patt":re.compile(r'\s+', re.UNICODE),
                      "replace":r" "},
        "inscription_whitespace_endline": {"patt":re.compile(r'(^\s|\s$)', re.UNICODE),
                      "replace":r""}}
  return rules

def clean_interpretive_rules():
  rules={"inscription_dubious_dot_subscript": {"patt":re.compile(r'\u0323', re.UNICODE),
                      "replace":r""},
        "inscription_edcs_number_three_both": {"patt":re.compile(r'\[3\]', re.UNICODE),
                      "replace":r"[-]"},
        "inscription_edcs_number_three_right": {"patt":re.compile(r'3\]', re.UNICODE),
                      "replace":r"-]"},
        "inscription_edcs_number_three_left": {"patt":re.compile(r'\[3', re.UNICODE),
                      "replace":r"[-"},
        "inscription_edcs_number_six_both": {"patt":re.compile(r'\[6\]', re.UNICODE),
                      "replace":r"[-]"},
        "inscription_edcs_number_one": {"patt":re.compile(r'[1]', re.UNICODE),
                      "replace":r" "},
        "inscription_edcs_quotes": {"patt":re.compile(r'\u0022', re.UNICODE),
                      "replace":r" "},
        "inscription_edcs_backslashes": {"patt":re.compile(r'\u005C\u005C', re.UNICODE),
                      "replace":r" "},
        "inscription_expanded_abbreviations_interpretive": {"patt":re.compile(r'[\(*\)]', re.UNICODE),
                      "replace":r""},
        "inscription_suppresion_remove_interpretive": {"patt":re.compile(r'{[^}]*}', re.UNICODE),
                      "replace":r""},
        "inscription_restoration_interpretive": {"patt":re.compile(r'[\[*\]]', re.UNICODE),
                      "replace":r""},
        "inscription_substitution_edh_interpretive": {"patt":re.compile(r'([α-ωΑ-Ωa-zA-Z])=([α-ωΑ-Ωa-zA-Z])', re.UNICODE),
                      "replace":r"\1"},
        "inscription_substitution_edh_interpretive_missing": {"patt":re.compile(r'([α-ωΑ-Ωa-zA-Z])*=([α-ωΑ-Ωa-zA-Z])', re.UNICODE),
                      "replace":r"\2"},
        "inscription_substitution_interpretive": {"patt":re.compile(r'[\<*\>]', re.UNICODE),
                      "replace":r""},
        "inscription_new_line": {"patt":re.compile(r'[\||\/|\/\/]', re.UNICODE),
                      "replace":r""},
        "inscription_interpunction_symbols": {"patt":re.compile(r'[=\+\,|\.|․|:|⋮|⁙|;|!|\-|—|–|#|%|\^|&|\~|@]', re.UNICODE),
                      "replace":r" "},
        "inscription_epigraphic_symbols": {"patt":re.compile(r'[❦|·|∙|𐆖|⏑|⏓|⏕]', re.UNICODE),
                      "replace":r""},
        "inscription_uncertainty_symbols": {"patt":re.compile(r'[\\?]', re.UNICODE),
                      "replace":r""},
        "inscription_arabic_numerals": {"patt":re.compile(r'[0-9]+', re.UNICODE),
                      "replace":r""},
        "inscription_unclosed_brackets": {"patt":re.compile(r'[\[|\{|\(|\)|\}|\]]', re.UNICODE),
                      "replace":r""},
        "inscription_edcs_que": {"patt":re.compile(r'(\w+)(que)\b', re.UNICODE),
                      "replace":r"\1 \2"},
        "inscription_edcs_vir": {"patt":re.compile(r'([I|V|X])(vir*)', re.UNICODE),
                      "replace":r"\1 \2"},
        "inscription_extra_blank": {"patt":re.compile(r'[ ]+', re.UNICODE),
                      "replace":r" "},
        "inscription_multi_whitespace": {"patt":re.compile(r'\s+', re.UNICODE),
                      "replace":r" "},
        "inscription_whitespace_endline": {"patt":re.compile(r'(^\s|\s$)', re.UNICODE),
                      "replace":r""},
                      }
  return rules


def clean(text, mode, rules, debug, show_inscription_transform):
  if debug:
    print(f"\n***\t{mode} to clean: {text}")

  for rule in rules:
    patt = rules[rule]["patt"]
    repl = rules[rule]["replace"]
    if debug and show_inscription_transform:
      print(f"\n-------\ncons rule: {rule}\nc\tpatt:{patt}\nc\trepl:{repl}\nc\tbefore:{text}\n")
    text = re.sub(patt, repl, text)
    if debug and show_inscription_transform:
      print(f"\tAfter: {text}")
  if debug:
    print(f"\n***\t{mode} cleaned: {text}")

  return text
