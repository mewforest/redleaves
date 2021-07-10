# Red Leaves / Красные Листья

This is the official offline copy of [redleaves.ru](http://redleaves.ru) 
([vk](https://vk.com/redleaves)) with some improvements.


>The repository also includes instructions and utilities for creating
custom offline site copies. 

---

## URL: [redleaves-ru.github.io](https://redleaves-ru.github.io/)

---

🇷🇺:
> Красные Листья — необычный литературный проект, объединяющий молодых авторов.

🇺🇸:
> Red Leaves is an unusual literary project that brings together young authors.
> Original language of the project is Russian.

### [Russian version](https://github.com/redleaves-ru/redleaves-ru.github.io/blob/main/README.ru.md)

## Improvements
- Added dark theme 🌙
- Restored all disappeared comments from HyperComments from 2012 (yes, even toxic threads) 🤯
- Restored music to works using Spotify 🎵
- New instant search 🔫🤠
- Added approximate age of the author for each literary work 👧🏻
- Removed ads and spam from comments 🚯
- Many small UI fixes (for example, the author's page now displays the entire list of his works) ✨

## How to crate your own offline copy

The following instructions can be applied to any website, not only Red Leaves:

1. Grab site with [Cyotek WebCopy](https://www.cyotek.com/downloads) 
   (free and open source). You can use project settings from `external/red leaves grabber config - cyotek webcopy.cwp`
2. Copy all downloaded content to `source`
3. You could change `pipe_stages` (function `process_html`) in `updater` to apply your own changes or for removing defaults, if needed.
4. Also, you could change global styles `external/style.css`, if needed.
5. Install all requirements for Python 3.6+ (from `requirements.txt`) and run `updater.py`.

### Additionals 

- If you need HyperComments extraction, see our [HyperComments Export](https://github.com/redleaves-ru/hypercomments-export)
   utility.
- If you need to use instant search, be note that all articles was exported to `external/articles.json` with vData Joomla! component.

## Short history of Red Leaves
> Sometime back in 2012, I came up with the idea to create a literary online magazine, and then
> I teamed up with my friends and classmates to create our own coolest resource. We did it!
> 
> More than 70 unique works have been published during this time. Red Leaves became a cozy version of a ficbook.ru, 
> but without a ton of the same fan fiction. It was like proza.ru, but without ugly UI design with own social network (like Facebook lmao)!
> Every post had tags, illustrations, and sometimes background music.
> 
> It was especially interesting when someone's literary work gained a lot of comments.
> 
> I am glad that the authors were able to become a part of this wonderful story!
> The most interesting days was from 2012 to 2015 and it delivers many unforgettable emotions to all participants and 
> readers of the Red Leaves magazine.


### Technical information

Red Leaves project is not maintained from 2016 year, the most active days was from 2012 to 2014, original site 
is offline from summer 2021. 

This copy does not include any sensitive data (hashed passwords, user emails, etc). Backend backup with 
database and Joomla! files will NEVER be uploaded or sold.


