import urllib
from pyPdf import PdfFileWriter, PdfFileReader
import os
from os.path import isfile, join
from bs4 import BeautifulSoup



def create(theurl):
    if theurl.split('/')[-1] == '':
        url = theurl
    else:
        url = theurl+'/'

    dir = url.split('/')[-2]

    try:
        os.stat(dir)
    except:
        os.mkdir(dir)

    html,count = '',1

    while 'Page not found' not in html:
        try:
            if count<10:
                base_url = url+'0000000%d'%count+'.pdf'
                urllib.urlretrieve(base_url,dir+'/' + str(count) + '.pdf')
            else:
                base_url = url+'000000%d'%count+'.pdf'
                urllib.urlretrieve(base_url,dir+'/' + str(count) + '.pdf')

            print base_url
            req = urllib.urlopen(base_url)
            html = req.read()
            count += 1
        except:
            req = urllib.urlopen(base_url)
            html = req.read()

    onlyfiles = [ f for f in os.listdir(dir) if isfile(join(dir,f)) ]
    d = {int(i.split('.')[0]): i for i in onlyfiles} 

    output = PdfFileWriter()
    for filename in d.values():
        try:
            output.addPage(PdfFileReader(file(dir+'/'+filename, 'rb')).getPage(0))
        except:
            pass
        

    out_path = dir+'/'+'output'

    try:
        os.stat(out_path)
    except:
        os.mkdir(out_path)
    
    output.write(file(out_path + '/' + url.split('/')[-2] + '.pdf','wb'))


ids = int(raw_input("Enter book ID: "))
magazine_url =  'http://www.pressacademyarchives.ap.nic.in/magazineframe.aspx?bookid='
later_url = 'http://www.pressacademyarchives.ap.nic.in/'
req = urllib.urlopen(magazine_url+str(ids))

b =  BeautifulSoup(req)

string = b.find(id="ContentPlaceHolder1_dListItems_frame_0")['src']
url = later_url+('/'.join(string.split('/')[:-1]))
create(url)
