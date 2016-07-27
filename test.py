import re

a = u"https://en.wikipedia.org/wiki/Computer_science"
post = re.split("https://[a-zA-Z]{0,3}\.",a)
dun = post[0].encode('utf-8')

if(len(post) ==  2):
	print post[1][0]
else:
	print post

url = u"https://ja.wikipedia.org/wiki/%E3%83%A1%E3%82%A4%E3%83%B3%E3%83%9A%E3%83%BC%E3%82%B8"
sum = 0
for letter in url:
	sum += ord(letter)

average =int(sum/len(url))
print average
