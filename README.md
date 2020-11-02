# 📚 wikipya
A simple python library for search pages and/or images in Wikipedia

## 🚀 Install
To install, run this code:
```
pip install wikipya
```
### 📦 Install module from source code
```
python setup.py install
```

## 🔩 Usage

```python
from wikipya.core import Wikipya
w = Wikipya("ru")
print(w.getPage("Камень"))
```

## 🛠 Methods
### 🔍 search
```python
>>> w.search("бан", limit=3)
```
```python
[
    ['Бан', 301867],
    ['Библиотека Российской академии наук', 717597],
    ['Бан (Интернет)', 61853]
]
```

### 🖼 getImageByPageName
```python
>>> w.getImageByPageName("Камень")
```
```python
{
    'source': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Two-parts_stone_nikogda_takih_ne_videl_vot.JPG/1000px-Two-parts_stone_nikogda_takih_ne_videl_vot.JPG',
    'width': 1000,
    'height': 687
}
```

### 🖼 getImagesByPageName
```python
>>> w.getImagesByPageName("Камень")
```
```python
{'batchcomplete': '', 'query': {'pages': {'2409325': {'pageid': 2409325, 'ns': 0, 'title': 'Камень', 'original': {'source': 'https://upload.wikimedia.org/wikipedia/commons/0/0c/Two-parts_stone_nikogda_takih_ne_videl_vot.JPG', 'width': 2173, 'height': 1492}}}}}
```

### 📜 getPage
```python
>>> w.getPage("Бан (Интернет)")
```
```html
<html><body><p><b>Бан</b> (англ. <span lang="en">ban</span>, <span>/bæn/</span> — запрещать, объявлять вне закона) — один из способов контроля над действиями пользователей в Интернете. Как правило, бан заключается в лишении или ограничении каких-либо прав пользователя (на создание/отправление новых сообщений или создание новых тем на веб-форуме, на отправление сообщений в чате, на комментирование в блогах, ограничение доступа к личным страницам и др.). Возможность введена в целях оградить интернет-сайт от троллей, спамеров, вандалов и прочих лиц, чьи сообщения вредят продуктивной работе ресурса.
</p><p>Бан обычно действует в рамках одного веб-сайта, группы (паблика) или личной страницы. Круг запретных действий, за которые на пользователя налагается бан, устанавливаются владельцами этого сайта.</p></body></html>
```

### 📒 parsePage
```python
>>> w.parsePage(w.getPage("Бан (Интернет)"))
```
```
'<b>Бан</b> (англ.\xa0ban, /bæn/\xa0— запрещать, объявлять вне закона)\xa0— один из способов контроля над действиями пользователей в Интернете. Как правило, бан заключается в лишении или ограничении каких-либо прав пользователя (на создание/отправление новых сообщений или создание новых тем на веб-форуме, на отправление сообщений в чате, на комментирование в блогах, ограничение доступа к личным страницам и др.). Возможность введена в целях оградить интернет-сайт от троллей, спамеров, вандалов и прочих лиц, чьи сообщения вредят продуктивной работе ресурса.\n'
```
