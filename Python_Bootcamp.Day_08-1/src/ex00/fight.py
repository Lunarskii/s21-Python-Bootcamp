import asyncio
from asyncio import sleep
from enum import Enum, auto
from random import choice, uniform


class Action(Enum):
    HIGH_KICK = auto()
    LOW_KICK = auto()
    HIGH_BLOCK = auto()
    LOW_BLOCK = auto()


class Agent:
    def __aiter__(self, health=5):
        self.health = health
        self.actions = list(Action)
        return self

    async def __anext__(self):
        return choice(self.actions)


async def get_neo_action(agent_action):
    await sleep(uniform(0.5, 1.0))
    if agent_action == Action.LOW_KICK:
        return Action.LOW_BLOCK
    elif agent_action == Action.HIGH_KICK:
        return Action.HIGH_BLOCK
    elif agent_action == Action.LOW_BLOCK:
        return Action.HIGH_KICK
    elif agent_action == Action.HIGH_BLOCK:
        return Action.LOW_KICK


async def fight_with_one(agent, agent_name):
    async for agent_action in agent:
        neo_action = await get_neo_action(agent_action)
        if neo_action in (Action.LOW_KICK, Action.HIGH_KICK):
            agent.health -= 1
        print(f'{agent_name}: {agent_action}, Neo: {neo_action}, Agent Health: {agent.health}')
        if agent.health == 0:
            break


async def fight():
    agent = Agent()
    await fight_with_one(agent, 'Agent')
    print('Neo wins!')


async def fightmany(n):
    agents = [Agent() for _ in range(n)]
    tasks = []

    for agent_index, agent in enumerate(agents):
        tasks.append(asyncio.create_task(fight_with_one(agent, f'Agent {agent_index + 1}')))
    await asyncio.gather(*tasks)
    print('Neo wins!')


if __name__ == '__main__':
    asyncio.run(fightmany(3))
