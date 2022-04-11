import argparse
from page_loader.page_loader import download
import os


def main():
    parser = argparse.ArgumentParser(description='Download page')
    parser.add_argument('url', type=str, help='set page url')
    parser.add_argument('-o', '--output', help='set path for output', type=str,
                        default=os.getcwd())
    args = parser.parse_args()

    download(args.url, args.output)


if __name__ == '__main__':
    main()
