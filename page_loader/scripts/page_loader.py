import argparse
from page_loader.page_loader import download
import os
from page_loader.logger import get_logger
import errno
import sys

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Download page')
    parser.add_argument('url', type=str, help='set page url')
    parser.add_argument('-o', '--output', help='set path for output',
                        type=str, default=os.getcwd())
    args = parser.parse_args()

    try:
        download(args.url, args.output)
    except PermissionError as error:
        logger.error(error)
        sys.exit(errno.EPERM)
    except FileNotFoundError as error:
        logger.error(error)
        sys.exit(errno.ENOENT)
    except ConnectionError as error:
        logger.error(error)
        sys.exit(errno.ECONNREFUSED)


if __name__ == '__main__':
    main()
