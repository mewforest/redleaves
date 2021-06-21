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
from distutils.dir_util import copy_tree
from typing import Dict, List, Tuple, Union

from bs4 import BeautifulSoup, Tag
from tqdm import tqdm

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
        for _ in concurrent.futures.as_completed(futures):
            pbar.update(1)
    pbar.close()


def load_metadata(etc_folder: str) -> Tuple[List[Dict[str, str]], List[Dict[str, Union[str, List[str]]]]]:
    """
    Loads metadata:

    1. Authors birth approximately (we do not show the exact date of birth)
    2. HyperComments commentaries extracted with our internal tool:
      https://github.com/redleaves-ru/hypercomments-export

    :param etc_folder: path to JSON's folder
    :return: author's metadata and commentaries
    """
    with open(os.path.join(etc_folder, 'hypercomments.json'), 'r', encoding='UTF-8') as f:
        comments = json.load(f)
    with open(os.path.join(etc_folder, 'authors.json.base64'), 'rb') as f:
        authors = json.loads(base64.decodebytes(f.read()))
    return authors, comments


def process_html(file_path: str, metadata: Tuple[List[Dict[str, str]], List[Dict[str, Union[str, List[str]]]]]) -> None:
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
        lambda sp, fp: add_hypercomments(sp, fp, comments=metadata[1])
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
    if file_path.endswith("default.htm"):
        html_content = """
        <div><h3>Ещё больше произведений в разделе <a href="index.phpoptioncom_contentviewcategorylayoutblogid9itemid264.htm">Проза</a> и 
        <a href="index.phpoptioncom_contentviewcategorylayoutblogid8itemid263.htm">Стихи</a></h3></div>
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


def add_hypercomments(soup: BeautifulSoup, file_name, comments):
    """
    Pipe that makes ...

    :param comments:
    :param file_name:
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

    comments_block = soup.select_one('.kmt-list')
    has_hc_comments = False
    if comments_block is not None:
        for comment in comments:
            comment_uri = re.match(r'https?://redleaves\.ru/.*/\d+([^#?]+)[^#]*#hcm=\d+', comment['url'])
            # print(comment_uri.group(1), '->', file_name, comment_uri.group(1) in file_name)
            if comment_uri is not None and comment_uri.group(1) in file_name:
                has_hc_comments = True
                # logging.info(f'Added HyperComment\'s commentary: {comment.text}')
                add_children(soup, '.kmt-list', generate_comment_html(comment), 'li', {})
    if has_hc_comments:
        remove_element(soup, ".kmt-empty-comment")
        insert_style(soup, """

.hc-comment {
  display: flex;
  font-size: 1rem;
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  font-size: 14px;
  line-height: 1.42857143;
  color: #333333;

  padding: 20px;
  border: 1px solid #e3e3e3;
  border-radius: 6px;
  border-top-left-radius: 6px;
  border-top-right-radius: 6px;
  border-bottom-right-radius: 6px;
  border-bottom-left-radius: 6px;
  -moz-border-radius: 6px;
  -webkit-border-radius: 6px;
}

.hc-avatar {
  display: block;
  width: 48px;
  height: 48px;
  border-radius: 100%;
}

.hc-content {
  font-size: 12p3;
  padding: 0 1rem;
}

.hc-header {
  font-size: 0.75rem;
  font-weight: 700;
  line-height: 1.125rem;
  color: #909090;
}

.hc-author {
  margin: 0;
  font-size: 0.9125rem;
  font-weight: 700;
  float: left;
  color: #222;
  cursor: pointer;
}

.hc-subheader {
  display: flex;
  align-items: flex-end;
}

.hc-date {
  margin: 0;
  margin-left: 1rem;
  color: #909090;
  font-size: 0.6875rem;
  margin-left: 0.3125rem;
  margin-bottom: 1px;
  font-weight: 700;
}

.hc-quote {
  font-size: 0.8125rem;
  line-height: 1rem;
  font-style: italic;
  color: #909090;
  margin-bottom: 0.625rem;
  background-color: #fff;
  padding: 0.625rem;
  border-left: 3px solid #d8cdcd;
}

.hc-text {
  font-size: 0.9375rem;
  line-height: 1.25rem;
  color: #222;
  margin-bottom: 0.625rem;
  word-wrap: break-word;
}

/* FIXES */

.kmt-list * {
    font-size: 14px !important;
    line-height: 1.4 !important;
}

.hc-header, .hc-date {
    font-size: 10px !important;
}

.hc-comment {
    padding-top: 10px !important;
    padding-left: 30px !important;
    border-top: 1px solid #ddd !important;
}

.hc-subheader {
    margin-bottom: 10px
}
""")


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
