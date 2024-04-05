from random import randint


def get_random_personality_traits():
    random_values = [randint(0, 100) for _ in range(5)]
    personality_traits = [value * 100 // sum(random_values) for value in random_values[:4]]
    personality_traits.append(100 - sum(personality_traits))
    return personality_traits


def turrets_generator():
    traits = ['neuroticism', 'openness', 'conscientiousness', 'extraversion', 'agreeableness']
    turret_instance = {
        'shoot': lambda: print('Shooting'),
        'search': lambda: print('Searching'),
        'talk': lambda: print('Talking')
    }
    turret_instance.update(dict(zip(traits, get_random_personality_traits())))
    return type('Turret', (object, ), turret_instance)


if __name__ == '__main__':
    turret = turrets_generator()
    print(turret.neuroticism)
    print(turret.openness)
    print(turret.conscientiousness)
    print(turret.extraversion)
    print(turret.agreeableness)
    turret.shoot()
    turret.search()
    turret.talk()
