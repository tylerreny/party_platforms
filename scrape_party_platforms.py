####
# Party Platform Scraper
####

'''This scraper collects party platforms going back to 1840 
from the UCSB American Presidency Project
website http://www.presidency.ucsb.edu/platforms.php'''

from lxml.cssselect import CSSSelector
import lxml.html
import csv
import unidecode

def get_platform_urls(url):
    
    #get links
    r = requests.get(url)
    tree = lxml.html.fromstring(r.text)
    sel = CSSSelector("a")
    res = sel(tree)
    lnks = [x.get('href') for x in res]
    
    #find just platform links
    save = []
    for link in lnks:
        if re.findall('pid=',link) :
            save.append(link)
        else:
            pass
                    
    return save

def fetch_platform_text(filename,url):
    
    #fetch urls for year
    urls = get_platform_urls(url)
    
    #open csv
    file = open(filename,'w')
    writer=csv.writer(file, delimiter=",", quoting=csv.QUOTE_ALL)
    writer.writerow(['year','party','text'])

    #parse each page
    i = 1
    for x in urls:
        i += 1
        r = requests.get(x)
        tree=lxml.html.fromstring(r.text)
        title=tree.xpath("//span[@class='paperstitle']")
        try:
            year = re.findall("([0-9]{4})",title[0].text_content())[0]  
        except:   
            year = ""
        party = title[0].text_content().strip()
        try:
            party = party.replace(year,'')
        except:
            party = party        
        text = tree.xpath("//span[@class='displaytext']")
        text = unidecode.unidecode(text[0].text_content()).replace("\n"," ").replace("\r","")
        print x,i
        writer.writerow([year,party,text])
    
fetch_platform_text('party_platforms.csv',"http://www.presidency.ucsb.edu/platforms.php")
