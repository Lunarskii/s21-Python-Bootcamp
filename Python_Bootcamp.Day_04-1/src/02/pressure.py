from random import randint
from time import sleep


def emit_gel(step):
    pressure = randint(50, 100)
    while True:
        pressure += randint(0, step) * (yield pressure)


def valve(gen):
    pressure = next(gen)
    sign = 1
    while True:
        print(f'Pressure = {pressure}')
        if pressure < 10 or pressure > 90:
            print('Emergency Break')
            gen.close()
            break
        elif pressure < 20 or pressure > 80:
            sign = -sign
        pressure = gen.send(sign)
        sleep(3)


if __name__ == '__main__':
    gen = emit_gel(7)
    valve(gen)
