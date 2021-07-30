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