<div align="center">
  <h1>📚 wikipya</h1>
  <h3>A simple async python library for search pages and images in wikis</h3>
</div><br>

## 🛠 Usage
```python
# Import wikipya
from wikipya import Wikipya

# Create Wikipya object with Wikipedia methods
wiki = Wikipya(lang="en").get_instance()

# or use other MediaEiki server (or other service, but this is'n fully supported now)

wikipya = Wikipya(url="https://ipv6.lurkmo.re/api.php", lurk=True, prefix="").get_instance()

# for use Lurkmore (russian). simple and fast

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
print(page.parsed)     # Get html cleared of link, and other non-formating tags

# Get image
image = await wiki.image(page.title)  # may not work in non-wikipedia services, check true prefix, or create issue

print(image.source)    # Image url
print(image.width)     # Image width
print(image.height)    # Image height
```

## 🎉 Features
- Full async
- Support of other instances of MediaWiki
- Support cleaning of HTML with TgHTML
- Uses models by [pydantic](https://github.com/samuelcolvin/pydantic)

## 🚀 Install
To install, run this code:
```
pip install wikipya
```
