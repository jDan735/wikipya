# 📚 wikipya
A simple python library for search pages and/or images in Wikipedia. Support async and sync mode.

## 🚀 Install
To install, run this code:
```
pip install wikipya
```

## 🛠 Usage
```python
# For sync import this
from wikipya.wiki import Wikipya

# For async this
# Is better solution but sync realisation is wrapper for async
from wikipya.aiowiki import Wikipya

# Create Wikipya object with wikipedia methods
wiki = Wikipya("en")

# Get a pages list from search
search = wiki.search("test")

# Get a pages list from opensearch
opensearch = wiki.opensearch("test")

# Get page class
# You can give to wiki.page() search item, title of page, page id

# Search item (supported ONLY wiki.search)
page = wiki.page(search[0])

# Page title
page = wiki.page("git")

# Pageid
page = wiki.page(800543)

print(page.html)       # Get page html
print(page.soup)       # Get parsed html (Beatiful Soup 4)
print(page.parsed)     # Get html cleared of link, and other non-formating tags 
print(page.fixed)      # [RU/UK] Свойство, в котором исправлены спорные слова (В/НА, Беларусь)

# Get page image
image = page.image()

print(image.source)    # Image url
print(image.width)     # Image width
print(image.height)    # Image height
```
