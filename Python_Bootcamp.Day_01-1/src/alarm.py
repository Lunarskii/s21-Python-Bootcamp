

def squeak_decorator(func):
    def squeak(*args):
        print("SQUEAK")
        return func(*args)
    return squeak
