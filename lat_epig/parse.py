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
import textwrap
from lat_epig.date_parse import parse_date
from lat_epig.text_parse import clean_conservative_rules, clean_interpretive_rules, clean
import json

COLUMNORDER = ["EDCS-ID",  #1
               "publication",  #2
               "province",  #3
               "place",  #4
               "dating_from", #5
               "dating_to",  #6
               "date_not_before",  #7
               "date_not_after",  #8
               "status",  #9
               "inscription",  #10
               "inscription_conservative_cleaning", #11
               "inscription_interpretive_cleaning",  #12
               "material",  #13
               "comment",  #14
               "latitude",  #15
               "longitude",  #16
               "language",  #17
               "photo",  #18
               "partner_link",  #19
               "extra_text",  #20
               "extra_html",  #21
               "raw_dating"] #22


FILENAME_TERM = {
  'EDCS': 'EDCS',
  'publication': 'pub',
  'province': 'prov',
  'place': 'place',
  'operator': 'op',
  'term2': 'term2',
  'dating_from': 'from',
  'dating_to': 'to',
  'inscription_genus': 'genus',
  'and_not_inscription_genus': 'not_genus',
  'to_file': 'to_file',
  'from_file': 'from_file',
  'debug': 'debug',
  'term1':'term1'  
}               
SUPPRESS_FILTER = "Link zurueck zur Suchseite"

@yaspin(text="Scraping site...")
def scrape(args, prevent_write=False, show_inscription_transform=False):
  searchTerm = args.term1
  #print("Searching for:")
  debug = False
  try:
    if (prevent_write or "debug" in args and args.__dict__['debug']):
      pprint(args)
      print("debug mode on")
      debug = True
  except:
    # Fix the stupid debug logging thing!!!
    pass

  searchString = []

  if "term1" in args.__dict__ and "%" not in args.__dict__['term1']:
    searchString.append("{}_{}".format(FILENAME_TERM['term1'], args.__dict__['term1']))

  if ("operator" in args.__dict__ and args.__dict__['operator'] != "and"):
    searchString.append("{}_{}".format(FILENAME_TERM['operator'], args.__dict__['operator']))

  if "term2" in args.__dict__ and args.__dict__['term2'] and "%" not in args.__dict__['term2']:
    searchString.append("{}_{}".format(FILENAME_TERM['term2'], args.__dict__['term2']))

  for k in args.__dict__:
    if args.__dict__[k] is not None:
      

      if k != "debug" and k != "term1" and k!="term2" and k!="operator":
        
      
        if type(args.__dict__[k]) == str:

          arg_str = "{}_{}".format(FILENAME_TERM[k], args.__dict__[k])
          #print(arg_str)
          searchString.append(arg_str)
        else:
          if len(args.__dict__[k]) > 2:
            words = []

            for w in args.__dict__[k]:
              phrase = []
              for word in w.split(" ")[:3]:
                if cleanword := re.sub(r"[^A-Za-z]+","",word[:2]):
                  phrase.append(cleanword)
              words.append('.'.join(phrase))
            results = ','.join(words)
            arg_str = "{}_{}({})".format(FILENAME_TERM[k], len(args.__dict__[k]), results)
          else:
            words = args.__dict__[k]
          # if args.__dict__[k] and len(args.__dict__[k]) < 3:
          #   results = '|'.join(args.__dict__[k])
          # else:
          #   words = args.__dict__[k][:1]

            results = ','.join(words)
            
            arg_str = "{}_{}".format(FILENAME_TERM[k], results)
          #print(arg_str)
          searchString.append(arg_str)            


  cleanSearchString='+'.join(searchString)
  cleanSearchString=re.sub("[^A-Za-z0-9+_,()|-]","", cleanSearchString)
  cleanSearchString=re.sub(r"\+term1_%","", cleanSearchString)
  if len(cleanSearchString) > 150:
    print("Filename too long, truncating...")
    cleanSearchString=f"{cleanSearchString[:150]}+++"
  #print(cleanSearchString)
  #print("Output filename: {}-{}-#inscriptions.tsv".format(datetime.date.today().isoformat(), cleanSearchString))
  
  #print("Searching for: \"%s\"." %  (searchTerm, primaryResult))

  # logger = logging.getLogger("mechanize")
  # logger.addHandler(logging.StreamHandler(sys.stdout))
  # logger.setLevel(logging.DEBUG)






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
        
        maplink = r.find(href=re.compile(".*map.php.*"))
        if maplink:
          
          latitude=re.search("latitude='([-0-9.]+)'", str(maplink['href']))
          longitude=re.search("longitude='([-0-9.]+)'", str(maplink['href']))
          place=re.search("ort='([^&]+)'", str(maplink['href']))
          if latitude:
            item['latitude']=latitude.group(1)
          if longitude:
            item['longitude']=longitude.group(1)
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
    html = re.sub(r"<b>dating:</b>(.*)<b>EDCS-ID",r"<div class='raw_dating'>\1</div><b>EDCS-ID", html)
    html = re.sub(r"<br/>\n([^<]*)<br/>",r"<div class='inscription'>\1</div>", html)
    html = re.sub(r"<br/>\n([^<]*)</p>",r"<div class='inscription'>\1</div></p>", html)
    html = re.sub(r"\n"," ", html)
    
    html = re.sub(r"<b>EDCS-ID:</b>([^<]*)",r"<div class='EDCS-ID'>\1</div>", html)
    html = re.sub(r"<b>province:</b>([^<]*)",r"<div class='province'>\1</div>", html)
    
    html = re.sub(r"<b>place:</b>[ \n]*(.*)</noscript>",r"<div class='place'>\1</noscript></div>", html)
    html = re.sub(r"<b>place:</b>[ \n]*(.*)<div",r"<div class='place'>\1</div><div", html)
    html = re.sub(r"<b>province:</b>([^<]*)",r"<div class='province'>\1</div>", html)
    html = re.sub(r"<b>inscription genus / personal status:</b>([^<]*)",r"<div class='status'>\1</div>", html)
    html = re.sub(r"<b>material:</b>([^<]*)",r"<div class='material'>\1</div>", html)
    html = re.sub(r"<b>comment:</b>(.*)</p>",r"<div class='comment'>\1</div>", html)
  
    
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
             "raw_dating":"raw_dating",
             "place:": "place",
             "EDCS-ID:": "EDCS-ID",
             "province:":"province",
             "inscription genus / personal status:": "status",
             "material:": "material",
             "comment:": "comment",
             "text:": "inscription",
             }


        #COLUMNORDER = ["EDCS-ID", "publication", "province", "place", "dating not before", "dating not after", "inscription status", "inscription", "Links", "latitude", "longitude", "TM Place"]
    for key in terms:             
      bs, item = itemExtract(bs, key, terms[key], item)
    


    # dating possibilities -100 to -1;  -70 to -31
    # dating ID: 72200182
    item['dating_from'] = item['dating_to'] = item['date_not_before'] = item['date_not_after'] = None

    parse_date(item, debug)

    


    if pub := bs.find("details"):
      if debug:
        print("details found")
        pprint(pub.get_text())
      item['comment'] = pub.get_text().replace('<br/>','\\n').strip()
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

    #print(item['inscription'])

    language_pattern = r"\"([A-Z]+)\""
    if type(item['inscription']) == str and re.search(language_pattern, item['inscription']):
      item['inscription'] = re.sub(language_pattern, pop_language, item['inscription'])

    opening_quote_language_pattern = r"\"([A-Z]+)(?:\"|\b)"
    if type(item['inscription']) == str and re.search(opening_quote_language_pattern, item['inscription']):
      item['inscription'] = re.sub(opening_quote_language_pattern, pop_language, item['inscription'])

    closing_quote_language_pattern = r"(?:\"|\b)([A-Z]+)\""
    if type(item['inscription']) == str and re.search(closing_quote_language_pattern, item['inscription']):      
      item['inscription'] = re.sub(closing_quote_language_pattern, pop_language, item['inscription'])


    if item['inscription']:
      if debug:
        pprint(item['inscription'])

      item['inscription_conservative_cleaning'] = clean(text=item['inscription'],
                                                        mode="conservative",
                                                        rules=clean_conservative_rules(),
                                                        debug=debug,
                                                        show_inscription_transform=show_inscription_transform)
      item['inscription_interpretive_cleaning'] = clean(text=item['inscription'],
                                                        mode="interpretive",
                                                        rules=clean_interpretive_rules(),
                                                        debug=debug,
                                                        show_inscription_transform=show_inscription_transform)
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

  inscriptionsFound = resultsSoup.findAll(string=re.compile("inscriptions found[^0-9]+([0-9]+)"))
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
  basefilename="{}-EDCS_via_Lat_Epig-{}-{}".format(datetime.date.today().isoformat().replace(":",""), cleanSearchString, len(output),"utf-8-sig")
  os.makedirs("output", exist_ok=True)
  if not prevent_write:
    with codecs.open(os.path.join("output", f"{basefilename}.json"), 'w', encoding='utf-8') as jsonfile:
      data = {'metadata':args.__dict__,
              'date':datetime.datetime.now().isoformat(),
              'data':output}
      json.dump(data, jsonfile)

    with codecs.open(os.path.join("output", f"{basefilename}.tsv"), 'w', encoding='utf-8') as tsvfile:
      writer = csv.DictWriter(tsvfile, fieldnames=COLUMNORDER, delimiter="\t")
      writer.writeheader()
      writer.writerows(output)
    
    #print("Done!")
    return(os.path.join("output", f"{basefilename}.tsv"))
  
  print("Debug mode on")
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

def main():
    print("Launch the Jupyter notebook.")
    parser = argparse.ArgumentParser(description="Scraping of http://db.edcs.eu/epigr/epi.php?s_sprache=en")


    # publication: 
    # province: 
    # place: 
    # search text 1: 
    #    and       or       and not    
    # search text 2: 
    # dating_from: 
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
    parser.add_argument('-ng',  "--and-not-inscription-genus", action='append', help="To exclude more than one genus, -ng more than once.")
    parser.add_argument("--to-file", help="save the search results as a webpage on the machine. Debug tool")
    parser.add_argument("--from-file", help="use the saved webpage instead of going to the manfred claus server. Debug.")
    parser.add_argument("--debug", action='store_true', help='Add the primary result debug column. Default (false)')
    
    parser.add_argument("term1", help="Search term, no flag is required. \n For phrases wrap them in \"\". For example, a one word search: platea. \nFor example, to search for Caesar divi Nervae, you write: ./parse.py \"Caesar divi Nervae\" to have Caesar... in the first search term. To have sophisticated wildcard matching (For example Caesar (anything) Nervae), ask Brian, or look at http://db.edcs.eu/epigr/hinweise/hinweis-en.html")

    args = parser.parse_args() #"platea"
    
      
    scrape(args)
if __name__ == "__main__":
  main()
