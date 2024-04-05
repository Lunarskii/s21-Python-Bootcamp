from pydantic import (
    BaseModel,
    Field,
    model_validator,
    ValidationError
)
import grpc
import test_pb2_grpc
import test_pb2
import argparse
from google.protobuf.json_format import MessageToJson

ALIGNMENT = {
    'ALIGNMENT_ALLY': 'Ally',
    'ALIGNMENT_ENEMY': 'Enemy'
}

SHIP_CLASS = {
    'CLASS_CORVETTE':
        {
            'class': 'Corvette',
            'length': (80, 250),
            'crew_size': (4, 10),
            'can_be_armed': True
        },
    'CLASS_FRIGATE':
        {
            'class': 'Frigate',
            'length': (300, 600),
            'crew_size': (10, 15),
            'can_be_armed': True
        },
    'CLASS_CRUISER':
        {
            'class': 'Cruiser',
            'length': (500, 1000),
            'crew_size': (15, 30),
            'can_be_armed': True
        },
    'CLASS_DESTROYER':
        {
            'class': 'Destroyer',
            'length': (800, 2000),
            'crew_size': (50, 80),
            'can_be_armed': True
        },
    'CLASS_CARRIER':
        {
            'class': 'Carrier',
            'length': (1000, 4000),
            'crew_size': (120, 250),
            'can_be_armed': False
        },
    'CLASS_DREADNOUGHT':
        {
            'class': 'Dreadnought',
            'length': (5000, 20000),
            'crew_size': (300, 500),
            'can_be_armed': True
        },
}


class Officer(BaseModel):
    first_name: str
    last_name: str
    rank: str


class Ship(BaseModel):
    alignment: str
    name: str
    ship_class: str = Field(serialization_alias='class')
    length: float
    crew_size: int
    armed: bool
    officers: list[Officer]

    @model_validator(mode='before')
    @classmethod
    def checking_parameters(cls, values):
        ship_class = values['ship_class']

        values['alignment'] = ALIGNMENT[values['alignment']]
        values['ship_class'] = SHIP_CLASS[ship_class]['class']

        if not (SHIP_CLASS[ship_class]['length'][0] <= values['length'] <= SHIP_CLASS[ship_class]['length'][1]):
            raise ValueError('Size of the ship is incorrect for this class')
        elif not (SHIP_CLASS[ship_class]['crew_size'][0] <= values['crew_size'] <= SHIP_CLASS[ship_class]['crew_size'][1]):
            raise ValueError('Size of the ship\'s crew is incorrect for this class')
        elif not SHIP_CLASS[ship_class]['can_be_armed'] and values['armed']:
            raise ValueError('This type of ship cannot be armed')

        if values.get('officers', 0) == 0:
            values['officers'] = []

        return values


def send_request(data):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = test_pb2_grpc.ServiceStub(channel)
        response = stub.SendData(test_pb2.Request(coords=data))
        return response


def main(data):
    msg = send_request(data)
    ships = []

    for ship in msg.ships:
        try:
            value = Ship.model_validate_json(MessageToJson(ship, preserving_proto_field_name=True))
        except ValidationError as e:
            continue
        else:
            ships.append(value)

    return ships


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('coords', type=float, nargs='+')
    args = parser.parse_args()
    ships = main(args.coords)
    [print(ship.model_dump_json(by_alias=True, indent=4)) for ship in ships]
