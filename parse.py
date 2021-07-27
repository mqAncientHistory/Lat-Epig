#!/usr/bin/env python3
# http://db.edcs.eu/epigr/epi.php?s_sprache=en

#EDCS-32300443
#tumulus?


import mechanicalsoup
import bs4
import re
import pprint
import sys, logging
import csv
#import cStringIO
import codecs
import argparse
import tkinter as tk
from lxml import etree
from pprint import pprint
import datetime
import os
import codecs
from clint.textui import progress
from yaspin import yaspin

COLUMNORDER = ["EDCS-ID", "publication", "province", "place", "dating from", "dating to", "date not before", "date not after", "status", "inscription", "inscription conservative cleaning", "inscription interpretive cleaning", "Material", "Comment", "Latitude", "Longitude", "TM Place", "language", "photo", "partner_link", "extra_text", "extra_html", "raw dating"]
SUPPRESS_FILTER = "Link zurueck zur Suchseite"

@yaspin(text="Scraping site...")
def scrape(args, prevent_write=False):
  searchTerm = args.term1
  #print("Searching for:")
  if "debug" in args and args.__dict__['debug']:
    pprint(args)
    debug = True
  else:
    debug = False

  searchString = []

  for k in args.__dict__:
    if args.__dict__[k] is not None:
      if k != "debug":
        if (k == "operator" and args.__dict__[k] != "and"):
          searchString.append("{}_{}".format(k, args.__dict__[k]))
        elif (k != "operator"):
          searchString.append("{}_{}".format(k, args.__dict__[k]))
  cleanSearchString='+'.join(searchString)
  cleanSearchString=re.sub("[^A-Za-z0-9+_%-]","", cleanSearchString)
  #print("Output filename: {}-{}-#inscriptions.tsv".format(datetime.date.today().isoformat(), cleanSearchString))
  
  #print("Searching for: \"%s\"." %  (searchTerm, primaryResult))

  # logger = logging.getLogger("mechanize")
  # logger.addHandler(logging.StreamHandler(sys.stdout))
  # logger.setLevel(logging.DEBUG)



  def clean_conservative(text):
    if debug:
      print(f"\n\n***\n\nconservative cleaning: {text}\n\n***\n\n")
    rules = {"inscription_expanded_abbreviations_conservative": {"patt":r"\([^(]*\)",
                        "replace":r""},
             "inscription_suppresion_superscripts_conservative": {"patt":r"{[^}]*}[⁰¹²³⁴⁵⁶⁷⁸⁹]+",
                                     "replace":r""},
             "inscription_suppresion_conservative": {"patt":r"[\{*\}]",
                                     "replace":r""},
             "inscription_restoration_conservative": {"patt":r"\[[^[]*\]",
                                     "replace":r""},
             "inscription_substitution_conservative": {"patt":r"\<[^<]*\>",
                                     "replace":r""},
             "inscription_substitution_edh_conservative": {"patt":r"([α-ωΑ-Ωa-zA-Z])=([α-ωΑ-Ωa-zA-Z])",
                                     "replace":r"\2"}}
    for rule in rules:
      patt = rules[rule]["patt"]
      repl = rules[rule]["replace"]
      if debug:
        print(f"\n-------\ncons rule: {rule}\nc\tpatt:{patt}\nc\trepl:{repl}\nc\tbefore:{text}\n")
      text = re.sub(patt, repl, text)
      if debug:
        print(f"\tAfter: {text}")
    if debug:
      print(f"\n\n***\n\nconservative cleaned: {text}")

    return text

  def clean_interpretive(text):
    rules={"inscription_expanded_abbreviations_interpretive": {"patt":r"[\(*\)]",
                        "replace":r""},}
    if debug:
      print(f"\n\n***\n\ninterpretive cleaning: {text}\n\n***\n\n")
    for rule in rules:
      patt = rules[rule]["patt"]
      repl = rules[rule]["replace"]
      if debug:
        print(f"\n-------\ninterp rule: {rule}\ni\tpatt:{patt}\ni\trepl:{repl}\ni\tbefore:{text}\n")
      text = re.sub(patt, repl, text)
      if debug:
        print(f"\tAfter: {text}")

    if debug:
      print(f"\n\n***\n\ninterpretive cleaned: {text}\n\n***\n\n")
    return text

  def parseItem(result):
    
    
    item={}
    for c in COLUMNORDER:
      item[c]=None
    for r in result:


      if type(r) == bs4.element.Tag:
        partner = r.find(href=re.compile("partner.php.*"))
        if partner and partner.get("href"):
          item['partner_link'] = f"http://db.edcs.eu/epigr/{partner['href']}"
        else:
          item['partner_link'] = ''
        # if partner:
        #   co=re.search("CO([0-9]+)", str(partner['href']))
        #   hd=re.search("(HD[0-9]+)", str(partner['href']))
        #   t=re.search("T([0-9]+)", str(partner['href']))
        #   n=re.search("N([0-9]+)", str(partner['href']))
        #   P=re.search("P([0-9]+)", str(partner['href']))
        #   oneae=re.search("1ae([0-9]+)-([0-9]+)", str(partner['href']))
        #   #print(partner['href'], hd, t)
        #   links=["http://db.edcs.eu/epigr/{}".format(partner['href'])]
        #   if oneae:
        #     links.append(f"http://db.edcs.eu/epigr/ae/{oneae.group(1)}/{oneae.group(1)}-{oneae.group(2)}.pdf")
        #     partner.extract()
        #   if P:
        #     links.append(f"https://epigraphy.packhum.org/text/{P.group(1)}")
        #     partner.extract()
        #   if hd:
        #     links.append("https://edh-www.adw.uni-heidelberg.de/edh/inschrift/{}".format(hd.group(1)))
        #     partner.extract()
        #   if t:
        #     links.append("https://www.trismegistos.org/text/{}".format(t.group(1)))
        #     partner.extract()
        #   if co:
        #     links.append("http://cil.bbaw.de/dateien/cil_view.php?KO=KO{}".format(co.group(1)))
        #     partner.extract()
        #   if n:
        #     links.append("http://www.edr-edr.it/edr_programmi/res_complex_comune.php?do=book&id_nr=EDR{}&partId=1".format(n.group(1)))
        #     partner.extract()
        #   if links:
        #     item['Links']=' | '.join(links)
        #   numlinks=partner['href'].count(';')+2
        #   # Because of the partnerpage, and no ; if there's only one.

        #   if len(links) != numlinks:
        #     with open("unknownDatabaseLink.csv","a") as unknown:
        #       unknown.write("{}\t{}\t{}\n".format(numlinks,len(links),partner['href']))
        maplink = r.find(href=re.compile(".*map.php.*"))
        if maplink:
          
          latitude=re.search("latitude='([-0-9.]+)'", str(maplink['href']))
          longitude=re.search("longitude='([-0-9.]+)'", str(maplink['href']))
          place=re.search("ort='([^&]+)'", str(maplink['href']))
          if latitude:
            item['Latitude']=latitude.group(1)
          if longitude:
            item['Longitude']=longitude.group(1)
          if place:
            item['place']=place.group(1)
        # Extra super hardcoded because I don't even know why.
        tm = re.search("http://www.trismegistos.org/place/[0-9]+", str(r))
        if tm:
          item['TM Place']=tm.group(0)
        pubPhoto = r.find(href=re.compile(".*bilder.php.*"))
        if pubPhoto:
          #print(pubPhoto)
          item['publication']=pubPhoto.text
          item['photo']="http://db.edcs.eu/epigr/bilder.php?{}".format(pubPhoto['href'])
          pubPhoto.extract()

    
    html = ""
    for r in result:
      html="{} {}".format(html, str(r))
    
    
    
    html = re.sub(u'\xa0', ' ', html)
    if not item.get("publication"):
        html = re.sub(r"<b>publication:</b>[ \n]*(.*)<b>dating",r"<div class='publication'>\1</div><b>dating", html)
        html = re.sub(r"<b>publication:</b>[ \n]*(.*)<b>EDCS",r"<div class='publication'>\1</div><b>EDCS", html) 
    else:
        html = re.sub(r"<b>publication:</b>",r"", html) 
    html = re.sub(r"<b>dating:</b>(.*)<b>EDCS-ID",r"<div class='raw dating'>\1</div><b>EDCS-ID", html)
    html = re.sub(r"<br/>\n([^<]*)<br/>",r"<div class='inscription'>\1</div>", html)
    html = re.sub(r"<br/>\n([^<]*)</p>",r"<div class='inscription'>\1</div></p>", html)
    html = re.sub(r"\n"," ", html)
    
    html = re.sub(r"<b>EDCS-ID:</b>([^<]*)",r"<div class='EDCS-ID'>\1</div>", html)
    html = re.sub(r"<b>province:</b>([^<]*)",r"<div class='province'>\1</div>", html)
    
    html = re.sub(r"<b>place:</b>[ \n]*(.*)</noscript>",r"<div class='place'>\1</noscript></div>", html)
    html = re.sub(r"<b>place:</b>[ \n]*(.*)<div",r"<div class='place'>\1</div><div", html)
    html = re.sub(r"<b>province:</b>([^<]*)",r"<div class='province'>\1</div>", html)
    html = re.sub(r"<b>inscription genus / personal status:</b>([^<]*)",r"<div class='status'>\1</div>", html)
    html = re.sub(r"<b>material:</b>([^<]*)",r"<div class='Material'>\1</div>", html)
    html = re.sub(r"<b>comment:</b>(.*)</p>",r"<div class='Comment'>\1</div>", html)
  
    
    bs = bs4.BeautifulSoup(html, 'lxml')
  
    def itemExtract(bs, searchterm, key, item):
      pub=bs.find(class_=key)
      if pub:
          #print(key, pub.get_text())
          item[key]=pub.get_text().strip()
          pub.extract()
        
#       if pub and pub.parent:
#         if pub.parent.next_sibling.strip():
#           item[key]=re.sub("\xa0+"," ",pub.parent.next_sibling.strip())
#           pub.parent.next_sibling.extract()
#         pub.extract()

      return (bs, item)


    terms = {"publication:":"publication",
             "raw dating":"raw dating",
             "place:": "place",
             "EDCS-ID:": "EDCS-ID",
             "province:":"province",
             "inscription genus / personal status:": "status",
             "material:": "Material",
             "comment:": "Comment",
             "text:": "inscription",
             }


        #COLUMNORDER = ["EDCS-ID", "publication", "province", "place", "dating not before", "dating not after", "inscription status", "inscription", "Links", "Latitude", "Longitude", "TM Place"]
    for key in terms:             
      bs, item = itemExtract(bs, key, terms[key], item)
    


    def date_min(old, new):
      if old and new:
        return min(int(old), int(new))
      elif old:
        return old
      else:
        return new

    def date_max(old, new):
      if old and new:
        return max(int(old), int(new))
      elif old:
        return old
      else:
        return new

    # dating possibilities -100 to -1;  -70 to -31
    # dating ID: 72200182
    if item["raw dating"]:
      if dates := re.findall(r" *(?![a-z1-9]+:)? *([0-9-]*(?!:))( to )?([0-9-]*(?!:));?", item["raw dating"]):
        # this is a multi-valued date 
        # dating:  a:  196 to 196;   b:  198 to 200;   c:  171 to 300;   d:  208 to 218;   e:  180 to 222;   f:  228 to 228;   g:  234 to 234;   h:  297 to 297;   i:  171 to 300;   j:  171 to 300;   k:  171 to 300         
        # EDCS-ID: EDCS-72200182
        # from: 196, to: 196, not-before: 196, not after: 300
        # dating:  a:  ;   b:  71 to 100;   c:  ;   d:           EDCS-ID: EDCS-32001032
        # from: 71, to: 100, not-before 71, not-after 100 
        # 24900077 a:  276 to 276;   b:  276 to 282
        # EDCS-75100087 3:  ;  -27 to 37
        #print("multi-valued dates")
        #pprint(dates)
        
          

        for date in dates:
          if date[0]:
            date_from = date[0]
            date_to = date[2]
            if not item['dating from']:
              item['dating from'] = int(date_from)
              item['date not before'] = int(date_from)
            if not item['dating to']:
              item['dating to'] = int(date_to)
              item['date not after'] = int(date_to)
            if debug:
              print(date, date_from, date_to, item.get('date not before', -9999), item['date not after'])
            item['date not before'] = date_min(date_from, item['date not before'])
            item['date not after'] = date_max(date_to, item['date not after'])
            #print(date, item['date not before'], item['date not after'])

            # if not item['date not before'] or date_from > item.get("date not before", -9999):
            #   item['date not before'] = date_from
            # if not item['date not after'] or date_to < item.get("date not after", 9999):
            #   item['date not after'] = date_to


      elif dates := re.findall(r"^ *([0-9-]+) to ([0-9-]+) *$", item["raw dating"]):
        # dating: -68 to -68         EDCS-ID: EDCS-24900077
        #print("single valued datespan")
        item['date not before'], item['date not after'] = dates[0]
        item['dating from'], item['dating to'] = dates[0]
      elif dates := re.findall(r"^ *([0-9-]+) *$", item["raw dating"]):
        # dating: -20         EDCS-ID: EDCS-41200809
        #print("single date")
        #pprint(dates)
        item['date not before'] = item['date not after'] = item['dating from'] = item['dating to'] = dates[0]        
      else:
        print(f"No date matched {item['EDCS-ID']}")
        if item["raw dating"]:
          pprint(item["raw dating"])
        item['dating from'] = item['dating to'] = item['date not before'] = item['date not after'] = ''
      if debug:
        pprint(item)
    else:
      item['dating from'] = item['dating to'] = item['date not before'] = item['date not after'] = ''


    if pub := bs.find("details"):
      print("details found")
      pprint(pub.get_text())
      item['Comment'] = pub.get_text().replace('<br/>','\\n').strip()
      pub.extract()




    item['extra_text'] = bs.get_text().strip()
    if item['extra_text']:
      item['extra_html'] = str(bs)
    else:
      item['extra_html'] = ""
    

#     pub=bs.find(text="place:")

#     if pub:
#       pub.extract()
#     pub=bs.find("noscript")

#     if pub:
#       pub.extract()

    

        
    # pub=bs.find(text=re.compile("\"[A-Z]+\""))
    languages=[]

    def pop_language(matchobj, languages=languages):
      languages.append(matchobj.group(1))
      return ''


    language_pattern = r"\"([A-Z]+)\""
    if type(item['inscription']) == str and re.search(language_pattern, item['inscription']):
      item['inscription'] = re.sub(language_pattern, pop_language, item['inscription'])

    if item['inscription']:
      pprint(item['inscription'])
      item['inscription conservative cleaning'] = clean_conservative(item['inscription'])
      item['inscription interpretive cleaning'] = clean_interpretive(item['inscription'])
    # while pub:    
    #   lang=re.search("\"([A-Z]+)\"", pub)
    #   if lang:
    #     languages.append(lang.group(1))
    #     pub.replace_with(re.sub("\"{}\"".format(lang.group(1)),"", pub))
    #   pub=bs.find(text=re.compile("\"[A-Z]+\""))

    item['language']=', '.join(languages)
    # item['inscription']=bs.text.strip()
    return item



  def itemSplit(item):
    split = item.split(": ",1)
    #print(split, len(split))
    if len(split) == 2:
      return dict([split])
    else:
      return None


  br =  mechanicalsoup.StatefulBrowser(
      soup_config={'features':'lxml'},
      
      #user_agent='MQEpigragrphyScraper/0.1'
  )

  if args.debug:
    br.set_verbose(2)

  if not args.from_file:
    br.open('http://db.edcs.eu/epigr/epi.php?s_sprache=en')

    br.select_form('[name="epi"]')

    br['p_episuch1'] = args.term1
    if args.EDCS:
      br['p_edcs_id'] = args.EDCS
    if args.publication:
      br['p_belegstelle'] = ' | '.join(args.publication)
    if args.province:
      br['p_provinz'] = ' | '.join(args.province)
    if args.place:
      br['p_ort'] = args.place
    if args.operator:
      if args.operator == "and":
        br['r_auswahl'] = "und"
      elif args.operator == "or":
        br['r_auswahl'] = "oder"
      elif args.operator == "not":
        br['r_auswahl'] = "und nicht"
    if args.term2:
      br['p_episuch2'] = args.term2
    if args.dating_from:
      br['p_dat_von'] = args.dating_from
    if args.dating_to:
      br['p_dat_bis'] = args.dating_to
    if args.inscription_genus:
      br['p_gattung1'] = ';'.join(args.inscription_genus)
    if args.and_not_inscription_genus:
      br['p_gattung2'] = ';'.join(args.and_not_inscription_genus)

    results = br.submit_selected()
    #print(results)



  else:
    with open(args.from_file, "r") as localfile:
      br.open_fake_page(localfile.read())
    

  resultsSoup = br.get_current_page()

  if args.to_file:
    with open(args.to_file, "w") as tofile:
      tofile.write(str(resultsSoup))

  with open("unknownDatabaseLink.csv","w") as unknown:
    unknown.write("")

  comments = resultsSoup.findAll(["script"])
  [comment.extract() for comment in comments]

  headers = resultsSoup.findAll(["h3"])
  #print(headers)
  [header.extract() for header in headers]


  endbutton = resultsSoup.findAll(style="font-size:110%;")
  #print("end", endbutton)
  [button.extract() for button in endbutton]

  inscriptionsFound = resultsSoup.findAll(text=re.compile("inscriptions found[^0-9]+([0-9]+)"))
  [inscription.parent.parent.extract() for inscription in inscriptionsFound]

  #print(resultsSoup)

  inscriptions=re.search("inscriptions found[^0-9]+0([0-9]+)", str(inscriptionsFound)).group(1)
  print("{} inscriptions found.".format(inscriptions))


  # tree = etree.parse(resultsSoup, etree.HTMLParser())

  # print(tree)
  #print("Inscriptions found %s".format(resultsSoup.xpath("//h3/p[b]/text()")))

  

  # scraped = []


  output = []
  for epigraphicResult in resultsSoup.find_all('p'):
    
    
    
    result = [epigraphicResult]

    for foo in epigraphicResult.next_siblings:
      
      searchString=re.search("<p", str(foo))
      if searchString:
        break

      result.append(foo)
    output.append(parseItem(result))
    
  # to_del=[]
  # for i, item in enumerate(output):
  #   if not item.get('EDCS-ID'):
  #       to_del.append(i)
        
  # for i in to_del:
  #   del output[i]

  output = [item for item in output if SUPPRESS_FILTER not in item.get('extra_html')]

  bad_output = [item for item in output if not item.get('EDCS-ID')]
  dump_bad = False
  if bad_output:
    for out in bad_output:
      if out['inscription'] or out['extra_html']:
        dump_bad = True
  
  if dump_bad:
    print("Some rows have been filtered")
    pprint(bad_output, indent=2)

  output = [item for item in output if item.get('EDCS-ID')]
  #output = filter()

  os.makedirs("output", exist_ok=True)
  if not prevent_write:
    with codecs.open(os.path.join("output", "{}-{}-{}.tsv").format(datetime.date.today().isoformat().replace(":",""), cleanSearchString, len(output),"utf-8-sig"), 'w', encoding='utf-8') as tsvfile:
      writer = csv.DictWriter(tsvfile, fieldnames=COLUMNORDER, delimiter="\t")
      writer.writeheader()
      writer.writerows(output)
    
    #print("Done!")
    return(os.path.join("output", "{}-{}-{}.tsv").format(datetime.date.today().isoformat().replace(":",""), cleanSearchString, inscriptions))
  
  print("brian")
  pprint(output)
  return(output)

  # pprint(output)

  # with open("%s.tsv" % (searchTerm), 'w', newline='', encoding='utf-8') as tsvfile:
  #   resultWriter = csv.writer(tsvfile, delimiter="\t", quotechar='"')
  #   #resultWriter.writerows(scraped)
  #   resultWriter.writerow(scrapedkeys)
    
  #   for line in scraped:    
  #     row=[]
  #     for k in scrapedkeys:
  #       if k in line:
  #         print(k, line[k])
  #         row.append(line[k])
  #       else:
  #         row.append(None)
  #     resultWriter.writerow(row)




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

#def test_digit_colon():
#  #  digit with colon 3:  ;  -27 to 37
#  #  EDCS-75100087 
#  args = argparse.Namespace(EDCS='75100087', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')
#  
#  test_output = scrape(args, prevent_write=True)
#  
#  assert test_output[0]['dating from'] == -27
#  assert test_output[0]['dating to'] == 37
#  assert test_output[0]['date not before'] == -27
#  assert test_output[0]['date not after'] == 37

#def test_digit_colon_empty():
#  #  digit with colon 1:
#  #  EDCS-74200019 
#  args = argparse.Namespace(EDCS='74200019', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')
#  
#  test_output = scrape(args, prevent_write=True)
#  
#  assert test_output[0]['dating from'] == 
#  assert test_output[0]['dating to'] == 
#  assert test_output[0]['date not before'] == 
#  assert test_output[0]['date not after'] == 

#def test_single_date():
#  #  dating: -20         
#  #  EDCS-ID: EDCS-41200809
#  
#  args = argparse.Namespace(EDCS='41200809', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')
#  
#  test_output = scrape(args, prevent_write=True)
#  
#  assert test_output[0]['dating from'] == -20
#  assert test_output[0]['dating to'] == -20
#  assert test_output[0]['date not before'] == -20
#  assert test_output[0]['date not after'] == -20

#def test_single_valued_datespan():
#  # dating: -68 to -68                  
#  #  EDCS-ID: EDCS-24900077
#  
#  args = argparse.Namespace(EDCS='24900077', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')
#  
#  test_output = scrape(args, prevent_write=True)
#  
#  assert test_output[0]['dating from'] == -68
#  assert test_output[0]['dating to'] == -68
#  assert test_output[0]['date not before'] == -68
#  assert test_output[0]['date not after'] == -68


#def test_missing_first_date():
#  # dating:  to 100                  
#  #  EDCS-ID: EDCS-34901010
#  
#  args = argparse.Namespace(EDCS='34901010', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')
#  
#  test_output = scrape(args, prevent_write=True)
#  
#  assert test_output[0]['dating from'] == 
#  assert test_output[0]['dating to'] == 100
#  assert test_output[0]['date not before'] == 
#  assert test_output[0]['date not after'] == 100


#def test_random__middle_date():
#  # # dating:  a:  ;   b:  71 to 100;   c:  ;   d:                             
#  #  EDCS-ID: EDCS-32001032
#  
#  args = argparse.Namespace(EDCS='34901010', publication=None, province=None, place=None, operator='and', term2=None, dating_from=None, dating_to=None, inscription_genus=None, and_not_inscription_genus=None, to_file=None, from_file=None, debug=True, term1='%')
#  
#  test_output = scrape(args, prevent_write=True)
#  
#  assert test_output[0]['dating from'] == 71
#  assert test_output[0]['dating to'] == 100
#  assert test_output[0]['date not before'] == 71
#  assert test_output[0]['date not after'] == 100



def main():
    print("Launch the Jupyter notebook.")
    parser = argparse.ArgumentParser(description="Scraping of http://db.edcs.eu/epigr/epi.php?s_sprache=en")


    # publication: 
    # province: 
    # place: 
    # search text 1: 
    #    and       or       and not    
    # search text 2: 
    # dating from: 
    #    to:    
    # inscription genus /
    # personal status: 
    # and not 
    # sorting: 
    #  publication       province    
    # advice
    # abbreviations
    # submit corrections
    # or new inscriptions
    
    parser.add_argument('-e',   "--EDCS")
    parser.add_argument('-p',   "--publication", action='append', help="to include more than one publication, use -p more than once")  
    parser.add_argument('-v',   "--province", action='append', help='To include more than one province, use -v more than once')  
    parser.add_argument('-l',   "--place")  
    parser.add_argument('-o',   "--operator", default='and', help="Default: and. Term Operator: and, or, not", choices=["and", "or", "not"])    
    parser.add_argument('-t',  "--term2")
    parser.add_argument('-df',  "--dating-from")
    parser.add_argument('-dt',  "--dating-to")
    parser.add_argument('-ig',  "--inscription-genus", action='append', help="To include more than one genus, -ig more than once.")
    parser.add_argument('-!ig',  "--and-not-inscription-genus")
    parser.add_argument("--to-file", help="save the search results as a webpage on the machine. Debug tool")
    parser.add_argument("--from-file", help="use the saved webpage instead of going to the manfred claus server. Debug.")
    parser.add_argument("--debug", action='store_true', help='Add the primary result debug column. Default (false)')
    
    parser.add_argument("term1", help="Search term, no flag is required. \n For phrases wrap them in \"\". For example, a one word search: platea. \nFor example, to search for Caesar divi Nervae, you write: ./parse.py \"Caesar divi Nervae\" to have Caesar... in the first search term. To have sophisticated wildcard matching (For example Caesar (anything) Nervae), ask Brian, or look at http://db.edcs.eu/epigr/hinweise/hinweis-en.html")

    args = parser.parse_args() #"platea"
    
      
    scrape(args)
if __name__ == "__main__":
  main()