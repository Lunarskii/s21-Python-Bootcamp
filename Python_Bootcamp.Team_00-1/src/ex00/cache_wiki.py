import wikipediaapi
import argparse
import logging
from neo4j import GraphDatabase
from db_config import db_config
from typing import TypedDict
from json import dump


class Wiki:
    class WikiPage:
        class Info(TypedDict, total=False):
            title: str
            links: list

        def __init__(self, wiki, page_name):
            self.page = wiki.page(page_name)
            self.page_links = [self.Info(title=title, links=[]) for title in self.page.links.keys()]

        def __len__(self) -> int:
            return len(self.page_links)

        def links(self, count_links=0) -> []:
            if count_links <= 0:
                return []
            return self.page_links[:count_links]

    def __init__(self, user_agent='Custom User-Agent/1.0', language='en'):
        self.wiki = wikipediaapi.Wikipedia(user_agent=user_agent, language=language)
        self.main_page = self.WikiPage.Info(title='', links=[])
        self.links_count = 0

    def exists(self, info: WikiPage.Info, value) -> bool:
        for page_value in info.values():
            if isinstance(page_value, list):
                if any(self.exists(dictionary, value) for dictionary in page_value):
                    return True
            elif page_value == value['title']:
                return True
        return False

    def links(self, page_name, depth=1, max_pages_count=1000):
        self.main_page['title'] = page_name
        self.main_page['links'] = self.internal_links(page_name, depth, max_pages_count)
        return self.main_page

    def internal_links(self, page_name, depth=1, max_pages_count=1000):
        if self.links_count >= max_pages_count or not depth:
            return []

        page = self.WikiPage(self.wiki, page_name)
        page_links = []

        for _ in range(depth):
            for link in page.links(max_pages_count - self.links_count):
                if self.links_count >= max_pages_count:
                    break
                if not self.exists(self.main_page, link):
                    self.links_count += 1
                    url_title = link['title'].replace(' ', '_')
                    logging.info(f'{self.links_count} Request URL: https://en.wikipedia.org/wiki/{url_title}')
                    page_links.append(self.WikiPage.Info(title=link['title'], links=self.internal_links(link['title'], depth - 1, max_pages_count)))

        return page_links


class DB:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def __del__(self):
        self.driver.close()

    def send_request(self, request, *args, **kwargs):
        with self.driver.session() as session:
            return session.run(request, *args, **kwargs)

    def import_dict(self, data: Wiki.WikiPage.Info, parent=None):
        for value in data.values():
            if isinstance(value, list):
                for dictionary in value:
                    self.import_dict(dictionary, parent)
            elif value is not None:
                self.send_request('CREATE (p:Page {title: $new_page})', new_page=value)
                if parent is not None:
                    self.send_request('MATCH (p1:Page {title: $parent}), (p2:Page {title: $new_page}) CREATE (p1)-['
                                      ':RELATIONSHIP]->(p2)', parent=parent, new_page=value)
                parent = value

    def clear(self):
        self.send_request('MATCH (n) DETACH DELETE n')


def export_to_db(data):
    db = DB(db_config['neo4j']['uri'], db_config['neo4j']['user'], db_config['neo4j']['password'])
    db.clear()
    db.import_dict(data)


def export_to_json(data):
    with open('wiki.json', 'w') as file:
        dump(data, file, indent=4)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)s %(levelname)s - %(message)s')
    logging.getLogger("wikipediaapi").setLevel(logging.WARNING)

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", help="page name", type=str, default='Python (programming language)')
    parser.add_argument("-d", help="search depth", type=int, default=3)
    args = parser.parse_args()

    wiki = Wiki()
    links = wiki.links(args.p, args.d)
    if wiki.links_count < 20:
        logging.info('Select a different start page')
    else:
        export_to_db(links)
        export_to_json(links)
