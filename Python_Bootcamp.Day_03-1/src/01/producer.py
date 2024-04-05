import redis
import logging
import json
import time
from random import randint, choice


def publish_transaction(r, m_from, m_to):
    message = {
        'metadata':
            {
                'from': None,
                'to': None
            },
        'amount': randint(-100000, 100000)
    }
    message['metadata']['from'] = m_from
    message['metadata']['to'] = m_to
    logging.info(message)
    r.publish('Transaction', json.dumps(message))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S', format='%(asctime)s - %(message)s')

    ids = [randint(10**9, 10**10) for _ in range(3)]
    r = redis.Redis(host='localhost', port=6379, db=0)
    while True:
        publish_transaction(r, *[choice(ids) for _ in range(2)])
        time.sleep(1)
