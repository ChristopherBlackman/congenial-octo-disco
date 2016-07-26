from bs4 import BeautifulSoup
import requests
import re

def getLinksImparative(url=""):
	
	fifo_list = EnqueueList(Node(str(url)))
	
	pop = fifo_list.pop()
	
	while(pop != None):
		print(str(pop))
		addNewLinksToQueueImparative(fifo_list,str(pop))
		pop = fifo_list.pop()
	
'''
	method : find all links on a web page and store them in the LinkList Class
	parameters : requires there to be a LinkedList with a url already assigned
'''
def addNewLinksToQueueImparative(fifo_list, parentLink = ""):
	try:
		response = requests.get(parentLink,timeout=(5))
	except:
		print "error - ", parentLink
		return
	sourceCode = response.text
	soup = BeautifulSoup(sourceCode,'html.parser')
	links = soup.find_all('a')
	for link in links:
		newLink = checkLinkImparative(link, parentLink)
		if(newLink != None):
			fifo_list.add(newLink)
	return

def checkLinkImparative(link, parent):
	unicode_string = unicode(link.get('href'))
	normal_string = unicode_string.encode('utf-8')
		
	if len(normal_string) <= 0:
		print 'string Less than equal to zero' , unicode_string
		return None
	
	post = re.findall('\?.*$',normal_string)
	if len(post) > 0:
		return None	
	
	ending_url = re.findall('\.\w*$',normal_string)
	if len(ending_url) > 0 and unwantedUrls(ending_url[0]):
		return None
	
	#case for pointers in web page
	if normal_string[0] == '#':
		return None
	#case for sorting out routing urls ('/') and ('//') urls (for some reason people add links like these)
	elif normal_string[0] == '/':
		stringObj = unicode_string.split('//',1)
		if len(stringObj) == 1:
			return Node(parent + stringObj[0], parent)
		elif len(stringObj) == 2:
			return Node('https://' + stringObj[1], parent)
	#default case (error prone here) needs to check if link is a link
	return Node(unicode_string,parent)

def unwantedUrls(url):
	#make it so that capitals and lowercases matter
	fileTypes = '.webm .png .jpg .bmp .svg .ogv .php .xml .pdf .gif'.split()
	for fileType in fileTypes:
		if str(fileType) == str(url):
			return True
	return False

class EnqueueList:
	#create a node link list
	#parameters(Node)
	def __init__(self,head=None):
		self.head = head
		self.back = None
		if(head != None):
			temp = head
			while(head.get_next() != None):
				temp = temp.get_next()
			self.back = temp
		return
	
	def add(self,node):
		if self.head != None:
			self.back.set_next(node)
			self.back = self.back.get_next()
		else:
			self.head = node
			self.back = node
		return

	def pop(self):
		returnVal = None
		if self.head != None:
			returnVal = self.head
			self.head = self.head.get_next()
			returnVal.set_next(None)
		return returnVal
		
class Node:
	def __init__(self,currentLink="",parent=""):
		self.currentLink = currentLink
		self.parent = parent
		self.next = None
	def __str__(self):
		return self.currentLink
	def set_next(self,next):
		self.next = next
	def get_next(self):
		return self.next
	def get_parent(self):
		return self.parent
	
getLinksImparative("https://en.wikipedia.org/wiki/Computer_science")