import os
from page_loader.modules import make_dashname_from_url
from page_loader.modules import file_save
from page_loader.modules import make_absolute_url
from page_loader.modules import is_link_to_page
from page_loader.modules import make_dir, read_page
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from page_loader.logger import get_logger
from progress.bar import Bar

logger = get_logger(__name__)
bar = Bar('Processing', max=5)


def download(url, dir=os.getcwd()):
    '''
    Save page locally and save local sources from this page
    Parameters:
        url: saved page url
        dir: directory to save page and sources.
             By default - current directory
    Return: path to page saved locally
    '''

    logger.info(f'start func with pageurl:{url}, output_dir:{dir}')

    logger.info('making page_file_name and page_local_path')
    page_file_name = make_dashname_from_url(url)
    page_file_path = os.path.join(dir, page_file_name)
    logger.info(f'page_file_name = {page_file_name}')
    logger.info(f'page_local_path = {page_file_path}')

    logger.info('making name and path of dir with files')
    folder_name = page_file_name[0:-5] + '_files'
    folder_path = os.path.join(dir, folder_name)
    logger.info(f'name {folder_name} and path {folder_path}')

    logger.info('start create dirrectory')
    make_dir(folder_path)
    logger.info('directory created')

    bar.next()

    logger.info('reading page')
    r = read_page(url)
    logger.info('page read')

    bar.next()

    soup = BeautifulSoup(r.text, 'html.parser')

    bar.next()

    tags_with_attr = {'img': 'src', 'link': 'href', 'script': 'src'}
    tags = tags_with_attr.keys()

    logger.info('changing links and saving sources')
    logger.info(f'page_url {url} and output_dir {folder_name}')

    for tag in soup.find_all(tags):
        attr = tags_with_attr[tag.name]

        if tag.has_attr(attr) and is_link_to_page(tag[attr], url):
            file_url_absolute = make_absolute_url(url, tag[attr])
            file_name = make_dashname_from_url(file_url_absolute)
            file_relative_path = os.path.join(folder_name, file_name)
            file_full_path = os.path.join(dir, file_relative_path)
            file_url = urljoin(url, tag[attr])
            r = read_page(file_url)
            file_save(r.content, file_full_path)
            tag[attr] = file_relative_path

    bar.next()

    logger.info('links changed and sources saved')

    logger.info('saving html with local links')
    with open(page_file_path, 'w') as saved_page:
        saved_page.write(soup.prettify())
    logger.info('html with local links saved')

    bar.next()

    return page_file_path
