from pprint import pprint
import re

def parse_date(item, debug):
  if item["raw dating"]:
    if dates := re.findall(r"( *(?![a-z1-9]+:)? *([0-9-]*(?!:))?( to )([0-9-]*(?!:));?)", item["raw dating"]):
      # this is a multi-valued date 
      # dating:  a:  196 to 196;   b:  198 to 200;   c:  171 to 300;   d:  208 to 218;   e:  180 to 222;   f:  228 to 228;   g:  234 to 234;   h:  297 to 297;   i:  171 to 300;   j:  171 to 300;   k:  171 to 300         
      # EDCS-ID: EDCS-72200182
      # from: 196, to: 196, not-before: 196, not after: 300
      # dating:  a:  ;   b:  71 to 100;   c:  ;   d:           EDCS-ID: EDCS-32001032
      # from: 71, to: 100, not-before 71, not-after 100 
      # 24900077 a:  276 to 276;   b:  276 to 282
      # EDCS-75100087 3:  ;  -27 to 37
      if debug:
        print("multi-valued dates")
        pprint(dates)
      
        

      for date in dates:
        if date[0]:
          date_from = date[1]
          date_to = date[3]
          if not item['dating from'] and date_from:
            item['dating from'] = int(date_from)
            item['date not before'] = int(date_from)
          if not item['dating to'] and date_to:
            item['dating to'] = int(date_to)
            item['date not after'] = int(date_to)
          if debug:
            print(date, date_from, date_to, item.get('date not before', -9999), item['date not after'])
          if item['date not before']:
            item['date not before'] = date_min(date_from, item['date not before'])
          if item['date not after']:
            item['date not after'] = date_max(date_to, item['date not after'])
          #print(date, item['date not before'], item['date not after'])

          # if not item['date not before'] or date_from > item.get("date not before", -9999):
          #   item['date not before'] = date_from
          # if not item['date not after'] or date_to < item.get("date not after", 9999):
          #   item['date not after'] = date_to


    elif dates := re.findall(r"^ *([0-9-]+) to ([0-9-]+) *$", item["raw dating"]):
      # dating: -68 to -68         EDCS-ID: EDCS-24900077
      if debug:
        print("single valued datespan")
      item['date not before'], item['date not after'] = [ int(x) for x in dates[0] ]
      item['dating from'], item['dating to'] = [ int(x) for x in dates[0] ]
    elif dates := re.findall(r"^ *([0-9-]+) *$", item["raw dating"]):
      # dating: -20         EDCS-ID: EDCS-41200809
      if debug:
        print("single date")
        pprint(dates)
      item['date not before'] = item['date not after'] = item['dating from'] = item['dating to'] = int(dates[0])
    elif dates := re.match(r"to ([0-9-]+)$", item["raw dating"]):
      # dating: to 100, EDCS-34901010
      if debug:
        print("blank start date")
        pprint(dates)
      item['date not before'] = item['dating from'] = None
      item['date not after'] = item['dating to'] = int(dates.group(1))
      
    else:
      print(f"No date matched {item['EDCS-ID']}")
      if item["raw dating"]:
        pprint(item["raw dating"])
  else:
    if debug and item['EDCS-ID']:
      print(f"No date matched {item['EDCS-ID']}")
      pprint(item["raw dating"])
    item['dating from'] = item['dating to'] = item['date not before'] = item['date not after'] = ''

    
def date_min(old, new):
  if old and new:
    return min(int(old), int(new))
  elif old:
    return int(old)
  else:
    return int(new)

def date_max(old, new):
  if old and new:
    return max(int(old), int(new))
  elif old:
    return int(old)
  else:
    return int(new)