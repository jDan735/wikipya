<div align="center">
  <h1>📚 wikipya</h1>
  <h3>A simple async python library for search pages and images in wikis</h3>
</div><br>

## 🛠 Usage
```python
# Import wikipya
from wikipya import Wikipya

# Create Wikipya object with wikipedia methods
wiki = Wikipya("en", lurk=False)

# or use other mediawiki server (or other service, but this is no supported now)

wikipya = Wikipya(url="https://ipv6.lurkmo.re/api.php", prefix="")

# for use lurkmore. simple and fast

# Get a pages list from search
search = await wiki.search("test")

# Get a pages list from opensearch
opensearch = await wiki.opensearch("test")

# Get page class
# You can give to wiki.page() search item, title of page, page id

# Search item (supported ONLY by wiki.search)
page = await wiki.page(search[0])

# Page title
page = await wiki.page("git")

# Pageid
page = await wiki.page(800543)

print(page.html)       # Get page html
print(page.soup)       # Get parsed html (Beatiful Soup 4)
print(page.parsed)     # Get html cleared of link, and other non-formating tags 
print(page.fixed)      # [RU/UK] Свойство, в котором исправлены спорные слова (В/НА, Беларусь)

# Get page image
image = await page.image()  # may not work in non-wikipedia services, check true prefix, or create issue

print(image.source)    # Image url
print(image.width)     # Image width
print(image.height)    # Image height
```

## 🎉 Features
- Full async
- Support of other instances of MediaWiki
- Support cleaning of HTML with TgHTML

## 🚀 Install
To install, run this code:
```
pip install wikipya
```
