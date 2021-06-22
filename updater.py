"""
updater.py

Script copies ./source to ./site and processes pipeline
"""
import base64
import concurrent.futures
import json
import logging
import os
import re
import webbrowser
from datetime import datetime
from distutils.dir_util import copy_tree
from pprint import pprint
from typing import Dict, List, Union

from bs4 import BeautifulSoup, Tag
from tqdm import tqdm


# Custom typings for metadata
class Typings:
    AuthorsBirths = List[Dict[str, str]]
    HyperComments = List[Dict[str, Union[str, List[str]]]]


# Metadata representation
class Metadata:
    def __init__(self, meta):
        self.authors: Typings.AuthorsBirths = meta['authors']
        self.comments: Typings.HyperComments = meta['comments']
        self.comments_css: str = meta['comments_css']


logging.basicConfig(level=logging.DEBUG)


def main() -> None:
    """
    Entrypoint for updater.py

    :return: None
    """
    from_folder, to_folder, etc_folder = "source", "site", "external"
    logging.info("Copying 'source' to 'site'..")
    copy_all_files(from_folder, to_folder)
    logging.info("Applying pipeline to HTML to 'site'..")
    apply_pipeline(to_folder, etc_folder)
    fix_styles(to_folder)
    logging.info("Done! Opening the result..")
    final_url = f'file://{os.path.abspath(to_folder)}/index.htm'
    webbrowser.open(final_url)


def fix_styles(output_folder: str):
    path_to_jomsocial_styles = f'{output_folder}/components/com_community/templates/jomsocial/assets/css/style.css'
    with open(path_to_jomsocial_styles, 'r', encoding='UTF-8') as f:
        css_content = f.read()
    css_content = css_content.replace(
        '.joms-focus__cover:before, .joms-hcard__cover:before {content:"";display:block;height:0;padding-top:37.5%; }',
        '.joms-focus__cover:before, .joms-hcard__cover:before {content:"";display:block;height:0;padding-top:0; }'
    )
    with open(path_to_jomsocial_styles, 'w', encoding='UTF-8') as f:
        f.write(css_content)


def copy_all_files(from_folder: str, to_folder: str) -> None:
    """
    Copies all source files to output folder.

    :param from_folder: path to folder with saved pages from redleaves.ru (e.g. Offline Explorer)
    :param to_folder: output folder
    :return: None
    """
    current_path = os.getcwd()
    if not all(root_folders in os.listdir(current_path) for root_folders in (from_folder, to_folder,)):
        logging.error(f"There is no important folders in current directory: {os.listdir(current_path)}")
        exit()
    copy_tree(from_folder, to_folder)


def apply_pipeline(root_dir: str, etc_folder: str) -> None:
    """
    Process pipe stages for each HTML file in parallel.

    :param root_dir: path to output folder
    :param etc_folder: path to JSON's folder
    :return: None
    """
    metadata = load_metadata(etc_folder)
    futures = []
    html_files = []
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if any(file.endswith(ext) for ext in ('.html', '.htm')):
                full_file_path = os.path.join(subdir, file)
                html_files.append(os.path.abspath(full_file_path))
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        for html_file in html_files:
            futures.append(executor.submit(process_html, file_path=html_file, metadata=metadata))
        pbar = tqdm(total=len(html_files))
        pbar.set_description("Processing html pages")
        for future in concurrent.futures.as_completed(futures):
            future.result()
            pbar.update(1)
    pbar.close()


def load_metadata(etc_folder: str) -> Metadata:
    """
    Loads and returns metadata in dictionary:

    [authors] Authors birth approximately (we do not show the exact date of birth)
    [comments] HyperComments commentaries extracted with our internal tool:
        https://github.com/redleaves-ru/hypercomments-export
    [comments_css] Custom CSS for HyperComments

    :param etc_folder: path to JSON's folder
    :return: metadata in dict()
    """
    with open(os.path.join(etc_folder, 'hypercomments.css'), 'r', encoding='UTF-8') as f:
        comments_css = f.read()
    with open(os.path.join(etc_folder, 'authors.json.base64'), 'rb') as f:
        authors = json.loads(base64.decodebytes(f.read()))
    with open(os.path.join(etc_folder, 'hypercomments.json'), 'r', encoding='UTF-8') as f:
        comments = json.load(f)
    for index, comment in enumerate(comments):
        comment_re = re.match(r'https?://redleaves\.ru/.*/\d+([^#?]+)[^#]*#hcm=\d+', comment['url'])
        comments[index]['uri'] = None if comment_re is None else comment_re.group(1)
    return Metadata({
        'authors': authors,
        'comments': comments,
        'comments_css': comments_css
    })


def process_html(file_path: str, metadata: Metadata) -> None:
    """
    Process pipeline for provided HTML file

    :param metadata:
    :param file_path: current HTML file
    :return: None
    """
    pipe_stages = [
        change_slogan,
        add_categories_to_homepage,
        fix_images,
        clean_commentaries_section,
        # fix_external_urls,
        remove_messages,
        make_images_clickable,
        improve_footer,
        lambda sp, fp: add_hypercomments(sp, fp, metadata.comments, metadata.comments_css)
    ]
    with open(file_path, 'r', encoding="UTF-8") as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, "html.parser")
    for stage in pipe_stages:
        stage(soup, file_path)
    with open(file_path, 'w', encoding="UTF-8") as f:
        f.write(str(soup))


# Pipes section


def change_slogan(soup: BeautifulSoup, *args):
    """
    Pipe that adds changes slogan in header

    :param soup: HTML body
    :return: None
    """
    replace_string(soup, '.site-slogan', 'Литературный проект, объединяющий молодых авторов. Архивная версия')


def add_categories_to_homepage(soup: BeautifulSoup, file_path: str) -> None:
    """
    Pipe that adds categories links to main page.

    :param soup: HTML body
    :param file_path: path to current HTML file
    :return: None
    """
    if file_path.endswith("index.htm"):
        html_content = """
        <div><h3>Ещё больше произведений в разделе <a href="proza.html">Проза</a> и 
        <a href="stikhi.htm">Стихи</a></h3></div>
        """
        add_children(soup, '.t3-content', html_content, 'div', {})


def fix_images(soup: BeautifulSoup, *args) -> None:
    """
    Pipe that fixes broken images.

    :param soup: HTML body
    :return: None
    """
    images_src = [
        [
            '[alt="97465406_plusBh1rgU9NG3H3fC9JhhFVKTDrA7sq4D2oWLA_0187f.jpg"]',
            'https://raw.githubusercontent.com/redleaves-ru/redleaves-ru.github.io/main/site/images/tony/97465406_plusbh1rgu9ng3h3fc9jhhfvktdra7sq4d2owla_0187f.jpg'
        ],
    ]
    for selector, src in images_src:
        replace_with_element(soup, selector, f'<img src="{src}" width="496" alt="image for article">')


def clean_commentaries_section(soup: BeautifulSoup, *args):
    """
    Pipe that removes "add commentary" section

    :param soup: HTML body
    :return: None
    """
    remove_element(soup, '.commentForm')
    remove_element(soup, '.kmt-addyours')


def remove_messages(soup: BeautifulSoup, *args):
    """
    Pipe that removes any Joomla! message from page

    :param soup: HTML body
    :return: None
    """
    remove_element(soup, '#system-message-container')


def make_images_clickable(soup: BeautifulSoup, *args):
    """
    Pipe that makes images clickable

    :param soup: HTML body
    :return: None
    """
    for article in soup.select('article'):
        article: Tag
        read_more = article.select_one('.readmore a')
        if read_more is not None:
            img = article.select_one('img')
            clickable_img_raw = f'<a href="{read_more.attrs["href"]}">{img}</a>'
            replace_with_element(soup, f"[src=\"{img.attrs['src']}\"]", clickable_img_raw)


def add_hypercomments(soup: BeautifulSoup, file_path: str, comments: Typings.HyperComments, style: str):
    """
    Pipe that adds HyperComments commentaries

    :param comments:
    :param file_path:
    :param soup: HTML body
    :return: None
    """

    def generate_comment_html(c: Dict[str, str]) -> str:
        return f"""
<div class="hc-comment">
  <img src="{c['avatar']}" class="hc-avatar">
  <div class="hc-content">
    <div class="hc-header">{c['title']}</div>
    <div class="hc-subheader">
      <h3 class="hc-author">{c['name']}</h3>
      <div class="hc-date">{c['date'].replace("T", " ")}</div>
    </div>
    <p class="hc-quote">{c['parent_text'] or '%REMOVE-EMPTY%'}</p>
    <p class="hc-text">{c['text']}</p>
  </div>
</div>
        """.replace('<p class="hc-quote">%REMOVE-EMPTY%</p>', '')

    file_name_uri = ""
    file_name_re = re.match(r'\d+(.*).html', file_path[file_path.rindex(os.path.sep) + 1:])
    if file_name_re is not None:
        file_name_uri = file_name_re.group(1)
    comments_block = soup.select_one('.kmt-list')
    has_hc_comments = False
    if comments_block is not None:
        for comment in comments:
            if comment['uri'] is None:
                continue
            if comment['uri'] == file_name_uri:
                has_hc_comments = True
                add_children(soup, '.kmt-list', generate_comment_html(comment), 'li', {})
    if has_hc_comments:
        remove_element(soup, ".kmt-empty-comment")
        insert_style(soup, style)


def improve_footer(soup: BeautifulSoup, *args):
    """
    Pipe .....

    :param soup: HTML body
    :return: None
    """
    remove_element(soup, '.copyright [style="display:none"]')
    footer_html = f"""
    <p>Архивная версия (<a href="https://github.com/redleaves-ru/redleaves-ru.github.io/edit/main/README.ru.md" target="_blank">что это значит?</a>).
    Обновлено: {datetime.now().isoformat().replace('T', ' ')[:-7]}.</p>
    """
    add_children(soup, '.copyright .custom', footer_html, 'div', {})


# Helper section


def replace_with_element(soup: BeautifulSoup, css_selector: str, replace_html: str) -> None:
    """
    Helper that replaces inner HTML of selected element

    :param soup: HTML body
    :param css_selector: CSS selector for html
    :param replace_html: new inner HTML
    :return: None
    """
    for target in soup.select(css_selector):
        target: Tag
        target.replace_with(BeautifulSoup(replace_html, 'html.parser'))


def replace_string(soup: BeautifulSoup, css_selector: str, replace_str: str) -> None:
    """
    Helper that replaces content of selected element

    :param soup: HTML body
    :param css_selector: CSS selector for html
    :param replace_str: new text
    :return: None
    """
    for target in soup.select(css_selector):
        target: Tag
        target.string = replace_str


def add_children(soup: BeautifulSoup, css_selector: str, child_html: str, wrap_tag: str,
                 wrap_attrs: Dict[str, str]) -> None:
    """
    Helper that creates and ads children element to selected element

    :param soup: HTML body
    :param css_selector: CSS selector for html
    :param child_html: children HTML
    :param wrap_tag: tag that wraps children HTML
    :param wrap_attrs: attributes for wrapper
    :return: None
    """
    for target in soup.select(css_selector):
        wrap_tag = soup.new_tag(wrap_tag)
        # child_tag.string = child_text
        for key, value in wrap_attrs.items():
            setattr(wrap_tag, key, value)
        target: Tag
        wrap_tag.append(BeautifulSoup(child_html, 'html.parser'))
        target.append(wrap_tag)


def remove_element(soup: BeautifulSoup, css_selector: str) -> None:
    """
    Helper that removes tag from the page

    :param soup: HTML body
    :param css_selector: CSS selector for html
    :return: None
    """
    for target in soup.select(css_selector):
        target: Tag
        target.decompose()


def replace_attributes(soup: BeautifulSoup, attribute: str, value: str, new_value: str) -> None:
    """
    Helper that replaces attributes on each element found by attribute

    :param new_value:
    :param value:
    :param attribute:
    :param soup: HTML body
    :return: None
    """
    for target in soup.find_all(attrs={attribute: value}):
        target: Tag
        target.attrs[attribute] = new_value


def insert_style(soup: BeautifulSoup, css_style: str) -> None:
    """
    Helper that adds CSS style to the page

    :param soup: HTML body
    :param css_style: CSS style
    :return: None
    """
    style_tag = BeautifulSoup(f'<style type="text/css">{css_style}</style>', features='html.parser')
    soup.select_one('head').append(style_tag)


if __name__ == '__main__':
    main()
