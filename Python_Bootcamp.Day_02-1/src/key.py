

class Key:
    passphrase = "zax2rulez"

    def __len__(self):
        return 1337

    def __str__(self):
        return "GeneralTsoKeycard"

    def __gt__(self, other):
        return other >= 9000

    def __getitem__(self, key):
        return 3


if __name__ == '__main__':
    key = Key()
    assert (len(key) == 1337)
    assert (key[404] == 3)
    assert (key > 9000)
    assert (key.passphrase == "zax2rulez")
    assert (str(key) == "GeneralTsoKeycard")
    print('The checks were completed successfully')
