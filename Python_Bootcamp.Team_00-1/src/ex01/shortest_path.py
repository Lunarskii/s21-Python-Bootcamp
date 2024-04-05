import os

from neo4j import GraphDatabase, Query
import argparse

# uri = 'neo4j+s://7406a279.databases.neo4j.io:7687'
uri = os.getenv("WIKI_FILE", "NOT SET")

username = "neo4j"
password = "ku3_nH04EwoCZL_81cvNbzLmMcFT7kIXOf2SE8HmEeA"

driver = GraphDatabase.driver(uri, auth=(username, password))

parser = argparse.ArgumentParser()

parser.add_argument("--from", dest="from_addr", help="from node", required=True)
parser.add_argument("--to", dest="to_addr", help="end node", required=True)
parser.add_argument("--non-directed", action="store_true", help="non directed edges")
parser.add_argument("-v", action="store_true", help="logging the path")
args = parser.parse_args()


def get_shortest_path():
    with driver.session() as session:
        direction = "" if args.non_directed else ">"
        query = f"""
            MATCH (start:Page {{title: $from_addr}}), (end:Page {{title: $to_addr}}),
            path = shortestPath((start)-[*]-{direction}(end))
            UNWIND nodes(path) AS node
            RETURN node.title AS title
        """
        return session.run(query, from_addr=args.from_addr, to_addr=args.to_addr).value("title")


def main():
    records = get_shortest_path()
    driver.close()

    if not records:
        print("Path not found")
        return
    elif args.v:
        formatted_string = " -> ".join(records)
        print(formatted_string)
    print(len(records)-1)


main()
