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

COLUMNORDER = ["EDCS-ID", "publication", "province", "place", "dating from", "dating to", "status", "inscription", "Material", "Comment", "Links", "Latitude", "Longitude", "TM Place", "language", "photo"]


def scrape(args):
  searchTerm = args.term1
  #print("Searching for:")
  #pprint(args)

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
  def parseItem(result):
    item={}
    for c in COLUMNORDER:
      item[c]=None
    for r in result:
      
      if type(r) == bs4.element.Tag:
        partner = r.find(href=re.compile("partner.php.*"))
        if partner:
          co=re.search("CO([0-9]+)", str(partner['href']))
          hd=re.search("(HD[0-9]+)", str(partner['href']))
          t=re.search("T([0-9]+)", str(partner['href']))
          n=re.search("N([0-9]+)", str(partner['href']))
          #print(partner['href'], hd, t)
          links=["http://db.edcs.eu/epigr/{}".format(partner['href'])]
          if hd:
            links.append("https://edh-www.adw.uni-heidelberg.de/edh/inschrift/{}".format(hd.group(1)))
          if t:
            links.append("https://www.trismegistos.org/text/{}".format(t.group(1)))
          if co:
            links.append("http://cil.bbaw.de/dateien/cil_view.php?KO=KO{}".format(co.group(1)))
          if n:
            links.append("http://www.edr-edr.it/edr_programmi/res_complex_comune.php?do=book&id_nr=EDR{}&partId=1".format(n.group(1)))
          if links:
            item['Links']=' | '.join(links)
          numlinks=partner['href'].count(';')+2
          # Because of the partnerpage, and no ; if there's only one.

          if len(links) != numlinks:
            with open("unknownDatabaseLink.csv","a") as unknown:
              unknown.write("{}\t{}\t{}\n".format(numlinks,len(links),partner['href']))
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
    bs = bs4.BeautifulSoup(html, 'lxml')


    def itemExtract(bs, searchterm, key, item):
      pub=bs.find(text=searchterm)
      if pub and pub.parent:
        if pub.parent.next_sibling.strip():
          item[key]=re.sub("\xa0+"," ",pub.parent.next_sibling.strip())
          pub.parent.next_sibling.extract()
        pub.extract()

      return (bs, item)


    terms = {"publication:":"publication",
             "place:": "place",
             "EDCS-ID:": "EDCS-ID",
             "province:":"province",
             "inscription genus / personal status:": "status",
             "material:": "Material",
             "comment:": "Comment"
             }


        #COLUMNORDER = ["EDCS-ID", "publication", "province", "place", "dating from", "dating to", "inscription status", "inscription", "Links", "Latitude", "Longitude", "TM Place"]
    for key in terms:             
      bs, item = itemExtract(bs, key, terms[key], item)
    

    pub=bs.find(text=re.compile("dating:"))
    if pub:
      try:
        item['dating from']=pub.parent.next_sibling.strip()
      except:
        item['dating from']="parse failed"
      try:
        item['dating to']=pub.parent.next_sibling.next_sibling.next_sibling.strip()
      except:
        item['dating to']="parse failed"
      
      pub.parent.next_sibling.next_sibling.next_sibling.extract()
      pub.parent.next_sibling.next_sibling.extract()
      pub.parent.next_sibling.extract()
      pub.parent.extract()

    pub=bs.find(text="place:")

    if pub:
      pub.extract()
    pub=bs.find("noscript")

    if pub:
      pub.extract()

    

        
    pub=bs.find(text=re.compile("\"[A-Z]+\""))
    languages=[]
    while pub:    
      lang=re.search("\"([A-Z]+)\"", pub)
      if lang:
        languages.append(lang.group(1))
        pub.replace_with(re.sub("\"{}\"".format(lang.group(1)),"", pub))
      pub=bs.find(text=re.compile("\"[A-Z]+\""))

    item['language']=', '.join(languages)
    item['inscription']=bs.text.strip()
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
    

  
  os.makedirs("output", exist_ok=True)
  
  with codecs.open(os.path.join("output", "{}-{}-{}.tsv").format(datetime.date.today().isoformat().replace(":",""), cleanSearchString, inscriptions,"utf-8-sig"), 'w', encoding='utf-8') as tsvfile:
    writer = csv.DictWriter(tsvfile, fieldnames=COLUMNORDER, delimiter="\t")
    writer.writeheader()
    writer.writerows(output)
  
  #print("Done!")
  return(os.path.join("output", "{}-{}-{}.tsv").format(datetime.date.today().isoformat().replace(":",""), cleanSearchString, inscriptions))

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
#   parser = argparse.ArgumentParser(description="Scraping of http://db.edcs.eu/epigr/epi.php?s_sprache=en")


#   # EDCS-ID: 
#   # publication: 
#   # province: 
#   # place: 
#   # search text 1: 
#   #    and       or       and not    
#   # search text 2: 
#   # dating from: 
#   #    to:    
#   # inscription genus /
#   # personal status: 
#   # and not 
#   # sorting: 
#   #  publication       province    
#   # advice
#   # abbreviations
#   # submit corrections
#   # or new inscriptions
  
#   parser.add_argument('-e',   "--EDCS")
#   parser.add_argument('-p',   "--publication", action='append', help="to include more than one publication, use -p more than once")  
#   parser.add_argument('-v',   "--province", action='append', help='To include more than one province, use -v more than once')  
#   parser.add_argument('-l',   "--place")  
#   parser.add_argument('-o',   "--operator", default='and', help="Default: and. Term Operator: and, or, not", choices=["and", "or", "not"])    
#   parser.add_argument('-t',  "--term2")
#   parser.add_argument('-df',  "--dating-from")
#   parser.add_argument('-dt',  "--dating-to")
#   parser.add_argument('-ig',  "--inscription-genus", action='append', help="To include more than one genus, -ig more than once.")
#   parser.add_argument('-!ig',  "--and-not-inscription-genus")
#   parser.add_argument("--to-file", help="save the search results as a webpage on the machine. Debug tool")
#   parser.add_argument("--from-file", help="use the saved webpage instead of going to the manfred claus server. Debug.")
#   parser.add_argument("--debug", action='store_true', help='Add the primary result debug column. Default (false)')
  
#   parser.add_argument("term1", help="Search term, no flag is required. \n For phrases wrap them in \"\". For example, a one word search: platea. \nFor example, to search for Caesar divi Nervae, you write: ./parse.py \"Caesar divi Nervae\" to have Caesar... in the first search term. To have sophisticated wildcard matching (For example Caesar (anything) Nervae), ask Brian, or look at http://db.edcs.eu/epigr/hinweise/hinweis-en.html")

#   args = parser.parse_args() #"platea"
  
    
#   scrape(args)
if __name__ == "__main__":
  main()