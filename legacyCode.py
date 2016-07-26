def checkLink(link, headLinkList):
	unicode_string = unicode(link.get('href'))
	normal_string = unicode_string.encode('utf-8')
		
	ending_url = re.findall('\.\w*$',normal_string)
	post = re.findall('\?.*$',normal_string)
	if len(post) > 0:
		print post , '	< post >'
		return
	if len(ending_url) > 0 and unwantedUrls(ending_url[0]):
		return
	if len(normal_string) <= 0:
		print 'string Less than equal to zero' , unicode_string
		return
	#case for pointers in web page
	if normal_string[0] == '#':
		return
	#case for sorting out routing urls and '//' urls
	elif normal_string[0] == '/':
		stringObj = unicode_string.split('//',1)
		if len(stringObj) == 1:
			headLinkList.appendLink(LinkList(headLinkList.getCurrentLink() + stringObj[0]))
		elif len(stringObj) == 2:
			headLinkList.appendLink(LinkList('https://' + stringObj[1]))
	#default case (error prone here) needs to check if link is a link
	else:
		headLinkList.appendLink(LinkList(unicode_string))
	return

'''
	method : find all links on a web page and store them in the LinkList Class
	parameters : requires there to be a LinkedList with a url already assigned
'''
def getLinkFromHead(headLinkList):
	try:
		response = requests.get(headLinkList.getCurrentLink(),timeout=2)
	except:
		return
	sourceCode = response.text
	soup = BeautifulSoup(sourceCode,'html.parser')
	links = soup.find_all('a')
	for link in links:
		checkLink(link, headLinkList)
	return

def getRidOfUselessLinks(listLinks):
	for link in listLinks:
		if link.getCurrentLink() == "None":
			print link.getCurrentLink()
			listLinks.remove(link)


def diveOneLevelDeeper(activeLinks,depth):
	newLinks = []
	getRidOfUselessLinks(activeLinks)
	print len(activeLinks)
	print activeLinks[0]
	print activeLinks[1]
	for link in activeLinks:
		print "Logging - ", link.getCurrentLink()
		getLinkFromHead(link)
		newLinks += link.getLinks()
	print depth
	diveOneLevelDeeper(newLinks,depth+1)

class LinkList:
	def __init__(self,currentLink):
		
		self.currentLink = currentLink
		self.nextLink = None
		
		self.links = list()
	def __str__(self):
		string = "head Link - " + self.getCurrentLink() + chr(10)
		for link in self.links:
			string += link.getCurrentLink() + chr(10)
		return string
	def appendLink(self,link):
		self.links.append(link)
		return
	def getLinks(self):
		return self.links
	def getCurrentLink(self):
		return self.currentLink
	

def getLinks():
	url = "https://www.animenfo.com/anime101.php"
	
	headLink = LinkList(url)
	print "Logging - ", headLink.getCurrentLink()
	getLinkFromHead(headLink)
	depth = 0
	diveOneLevelDeeper(headLink.getLinks(),depth)
	