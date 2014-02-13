from readability.readability import Document
import urllib
import MLStripper
html = urllib.urlopen('http://techcrunch.com/2014/01/30/microsoft-ceo/').read()
readable_article = Document(html).summary()
readable_title = Document(html).short_title()

print MLStripper.strip_tags(readable_article).replace('\n', '')