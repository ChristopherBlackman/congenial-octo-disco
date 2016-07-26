import re

a = " https://en.wikipedia.org/wiki/Computer_science/w/index.php?title=Computer_science&action=edit&section=1"
post = re.findall('\?.*$',a)

print post
