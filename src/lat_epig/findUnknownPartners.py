#!/usr/bin/env python3

import csv
from pprint import pprint
import re

unique_references = set()

with open('unknownDatabaseLink.csv') as csvfile:
  csvreader = csv.reader(csvfile, delimiter="\t")
  for line in csvreader:
    blah = re.split(r"[?&;=]", line[2])
    del blah[0:4]
    #pprint(blah)
    for item in blah:
      unique_references.add(item)

prefix = ""

for ref in sorted(unique_references):
  db = re.match(r"(^[^0-9]+)", ref)
  if db:
    if db.group(1) != prefix:
      pprint(db.group(1))
      print(f"\thttp://db.edcs.eu/epigr/partner.php?s_language=en&param={ref}")
      prefix = db.group(1)
  elif "1ae" in ref:
    pass
  else:
    print(f"nomatch {ref}")
    print(f"\thttp://db.edcs.eu/epigr/partner.php?s_language=en&param={ref}")
      