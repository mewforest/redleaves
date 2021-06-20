"""
updater.py

Script copies ./source to ./site and processes pipeline
"""
import base64
import concurrent.futures
import json
import logging
import os
import webbrowser
from distutils.dir_util import copy_tree
from glob import iglob
from itertools import chain
from pprint import pprint
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
    logging.info("Done! Opening the result..")
    webbrowser.open(f'file://{os.path.abspath(to_folder)}/index.htm')


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


def process_html(file_path: str, metadata) -> None:
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
        remove_messages
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


# def fix_external_urls(soup: BeautifulSoup, *args):
#     """
#     Pipe that fixes some external urls, e.g. vk.com/redleaves
#
#     :param soup: HTML body
#     :return: None
#     """
#     replace_attributes(soup, 'href', "../vk.com/redleaves", "https://vk.com/redleaves")


def remove_messages(soup: BeautifulSoup, *args):
    """
    Pipe that removes any Joomla! message from page

    :param soup: HTML body
    :return: None
    """
    remove_element(soup, '#system-message-container')


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


def add_children(soup: BeautifulSoup, css_selector: str, child_html: str, wrap_tag: str, wrap_attrs: Dict[str, str]) -> None:
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


if __name__ == '__main__':
    main()
