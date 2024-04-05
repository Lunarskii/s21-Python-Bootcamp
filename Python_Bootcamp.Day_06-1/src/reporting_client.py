import grpc
import test_pb2_grpc
import test_pb2
import argparse
import json


ALIGNMENT = {
    1: 'Ally',
    2: 'Enemy'
}

SHIP_CLASS = {
    1: 'Corvette',
    2: 'Frigate',
    3: 'Cruiser',
    4: 'Destroyer',
    5: 'Carrier',
    6: 'Dreadnought'
}


def create_dict(ship):
    return {
        'alignment': ALIGNMENT[ship.alignment],
        'name': ship.name,
        'class': SHIP_CLASS[ship.ship_class],
        'length': ship.length,
        'crew_size': ship.crew_size,
        'armed': ship.armed,
        'officers': [
            {
                'first_name': officer.first_name,
                'last_name': officer.last_name,
                'rank': officer.rank
            } for officer in ship.officers
        ]
    }


def send_request(data):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = test_pb2_grpc.ServiceStub(channel)
        response = stub.SendData(test_pb2.Request(coords=data))
        return response


def print_json(data):
    print(json.dumps(data, indent=4))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('coords', type=float, nargs='+')
    args = parser.parse_args()
    msg = send_request(args.coords)
    [print_json(create_dict(ship)) for ship in msg.ships]
