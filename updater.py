"""
updater.py

Script copies ./source to ./site and processes pipeline
"""
import concurrent.futures
import logging
import os
import webbrowser
from distutils.dir_util import copy_tree
from typing import Dict

from bs4 import BeautifulSoup, Tag
from tqdm import tqdm

logging.basicConfig(level=logging.DEBUG)


def main():
    from_folder, to_folder = "source", "site"
    logging.info("Copying 'source' to 'site'..")
    copy_all_files(from_folder, to_folder)
    logging.info("Applying pipeline to HTML in 'site'..")
    apply_pipeline(to_folder)
    logging.info("Done! Opening the result..")
    webbrowser.open(f'file://{os.path.abspath(to_folder)}/default.htm')


def copy_all_files(from_folder: str, to_folder: str) -> None:
    current_path = os.getcwd()
    if not all(root_folders in os.listdir(current_path) for root_folders in (from_folder, to_folder,)):
        logging.error(f"There is no important folders in current directory: {os.listdir(current_path)}")
        exit()
    copy_tree(from_folder, to_folder)


def apply_pipeline(root_dir: str):
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        futures = []
        html_files = []
        for file in os.listdir(root_dir):
            if any(file.endswith(ext) for ext in ('.html', '.htm')):
                html_files.append(os.path.abspath(f'{root_dir}/{file}'))
        for file in html_files:
            futures.append(executor.submit(process_html, file_path=file))
        pbar = tqdm(total=len(html_files))
        pbar.set_description("Processing html pages")
        for future in concurrent.futures.as_completed(futures):
            pbar.update(1)
            # print(future.result())
        pbar.close()


def process_html(file_path: str):

    pipe_stages = [
        change_slogan,
        add_categories_to_homepage,
        fix_images,

    ]

    with open(file_path, 'r', encoding="UTF-8") as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, "html.parser")
    for stage in pipe_stages:
        stage(soup, file_path)
    with open(file_path, 'w', encoding="UTF-8") as f:
        f.write(str(soup))


def change_slogan(soup: BeautifulSoup, file_path: str):
    replace_string(soup, '.site-slogan', 'Литературный проект, объединяющий молодых авторов. Архивная версия')


def add_categories_to_homepage(soup: BeautifulSoup, file_path: str):
    if file_path.endswith("default.htm"):
        html_content = """
        <div><h3>Ещё больше произведений в разделе <a href="index.phpoptioncom_contentviewcategorylayoutblogid9itemid264.htm">Проза</a> и 
        <a href="index.phpoptioncom_contentviewcategorylayoutblogid8itemid263.htm">Стихи</a></h3></div>
        """
        add_children(soup, '.t3-content', html_content, 'div', {})


def fix_images(soup: BeautifulSoup, file_path: str):
    images_src = [
        [
            '[data-src="images/281608_kosmos_-zemlya_-luna_-planety_-tuchi_3200x2000_www.GdeFon.ru_07c60.jpg"]',
            'images/281608_kosmos_-zemlya_-luna_-planety_-tuchi_3200x2000~1.jpg'
        ],
        [
            '[data-src="../fc00.deviantart.net/fs20/f/2007/279/5/d/blue_eyes_by_manicfairytale.jpg"]',
            'images/d13oplp-65d9d702-0fc1-4285-8266-d402be1ed612.jpgtoken_1.jpg'
        ]
    ]
    for selector, src in images_src:
        replace_with_element(soup, selector, f'<img src="{src}" width="496" alt="image for article">')


def replace_with_element(soup: BeautifulSoup, css_selector: str, replace_html: str):
    for target in soup.select(css_selector):
        target: Tag
        target.replace_with(BeautifulSoup(replace_html, 'html.parser'))


def replace_string(soup: BeautifulSoup, css_selector: str, replace_str: str):
    for target in soup.select(css_selector):
        target: Tag
        target.string = replace_str


def add_children(soup: BeautifulSoup, css_selector: str, child_html: str, child_tag: str, child_attrs: Dict[str, str]):
    for target in soup.select(css_selector):
        child_tag = soup.new_tag(child_tag)
        # child_tag.string = child_text
        for key, value in child_attrs.items():
            setattr(child_tag, key, value)
        target: Tag
        child_tag.append(BeautifulSoup(child_html, 'html.parser'))
        target.append(child_tag)


if __name__ == '__main__':
    main()
