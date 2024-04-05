import redis
import logging
import json
import argparse


def parse_strings(value):
    return [i for i in value.split(',')]


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S', format='%(asctime)s - %(message)s')

    parser = argparse.ArgumentParser()
    parser.add_argument('-e', type=parse_strings)
    bad_guys = vars(parser.parse_args())['e']

    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    pubsub = r.pubsub()
    pubsub.subscribe('Transaction')

    for message in pubsub.listen():
        if message['type'] == 'message':
            message = json.loads(message.get('data'))
            if bad_guys and message['amount'] > 0 and str(message['metadata']['to']) in bad_guys:
                message['metadata']['from'], message['metadata']['to'] = message['metadata']['to'], message['metadata']['from']
            logging.info(message)
