import asyncio
import random

from factories.game_factory import create_game
from game_context import GameContext
from models.consumable_model import ConsumableConfig
from models.enemy_model import EnemyConfig
from models.game_model import GameConfig, GameModel, InputType
from models.input_model import Direction, InputActionModel, InputSelectModel
from models.melee_weapon_model import MeleeWeaponConfig
from models.player_model import PlayerConfig
from models.shared import PointModel
from models.upgrade_model import (ExpConsumeRadiusUpgradeConfig,
                                  ExpConsumeRateUpgradeConfig,
                                  HealRateUpgradeConfig, HealthUpgradeConfig)
from objects.player import Player
from utils.utils import async_input, get_uuid

test_config: GameConfig = GameConfig(
    seed='test',
    players=[
        PlayerConfig(
            name='Player',
            position=PointModel(x=0, y=0),
            health=100,
            vision_radius=5,
            exp_level_map=[10, 20, 30],
            exp_consume_radius=1,
            weapon=MeleeWeaponConfig(type='sword', damage=5),
            upgrades=[
                HealthUpgradeConfig(name='Helth +10', value=10, next_upgrades=[
                    HealthUpgradeConfig(name='Health +20', value=20, next_upgrades=[
                        HealthUpgradeConfig(
                            name='Health +50', value=50, next_upgrades=[]),
                    ]),
                ]),
                HealRateUpgradeConfig(
                    name='Heal Rate +10%', value=0.1, next_upgrades=[]),
                ExpConsumeRadiusUpgradeConfig(name='XP consume radius +1', value=1, next_upgrades=[
                    ExpConsumeRadiusUpgradeConfig(name='XP consume radius +1', value=1, next_upgrades=[
                        ExpConsumeRadiusUpgradeConfig(
                            name='XP consume radius +2', value=2, next_upgrades=[])
                    ])
                ]),
                ExpConsumeRateUpgradeConfig(name='XP consume rate +20%', value=0.2, next_upgrades=[
                    ExpConsumeRateUpgradeConfig(
                        name='XP consume rate +10%', value=0.1, next_upgrades=[]),
                ]),
            ]
        )
    ],
    enemies=[
        EnemyConfig(
            name='Enemy',
            position=PointModel(x=0, y=0),
            health=10,
            tags=set(['enemy']),
            weapon=MeleeWeaponConfig(type='teeth', damage=10),
            initiative=0.75,
            drop_object=ConsumableConfig(
                name='exp',
                type='exp',
                position=PointModel(x=0, y=0),
                value=10
            )
        )
    ]
)

grass = [PointModel(x=random.randint(-50, 50), y=random.randint(-50, 50))
         for _ in range(200)]


def render_game(state: GameModel):
    radius = 5

    if state.players and len(state.players):
        player = state.players[0]
        enemies = state.enemies or list()
        consumables = state.consumables or list()

        print(f'\rPlayer: {player.health}HP {
              player.experience}XP {player.level}LVL')

        for k in range(player.position.y - radius, player.position.y + radius + 1):
            row = []
            for i in range(player.position.x - radius, player.position.x + radius + 1):
                if (i == player.position.x and k == player.position.y):
                    row.append('P')
                else:
                    for enemy in [e for e in enemies if e.health > 0]:
                        if i == enemy.position.x and k == enemy.position.y:
                            row.append('E')
                            break
                    else:
                        for consumable in [c for c in consumables if not c.consumed]:
                            if i == consumable.position.x and k == consumable.position.y:
                                if 'exp' in consumable.tags:
                                    row.append('e')
                                    break
                                elif 'health' in consumable.tags:
                                    row.append('h')
                                    break
                        else:
                            for g in grass:
                                if g.x == i and g.y == k:
                                    row.append('~')
                                    break
                            else:
                                row.append('-')
            print(' '.join(row))


def main():
    with GameContext(get_uuid()) as game_id:
        game = create_game(game_id, test_config)

        player = list(game.objects.find_by_tag('player'))[0]

        if not isinstance(player, Player):
            raise Exception('Player is invalid')

        async def input_direction():
            value = await async_input('Enter direction (left, up, right, down): ')
            try:
                game.send_to_input(InputActionModel(
                    player_name=player.name, input=Direction(value)))
            except:
                game.send_to_input(InputActionModel(
                    player_name=player.name, input=None))

        async def input_select():
            upgrades = list(player.upgrades.get_next_upgrades())
            random.shuffle(upgrades)
            for ind, upg in enumerate(upgrades[:4]):
                print(f'[{ind}] Upgrade {upg.name}')
            value = await async_input('Select PowerUp (0, 1, 2, 3): ')

            upgrade_id = upgrades[int(value)].id

            try:
                game.send_to_input(InputSelectModel(
                    player_name=player.name, input=upgrade_id))
            except:
                game.send_to_input(InputSelectModel(
                    player_name=player.name, input=None))

        def output_listener(state: GameModel):
            if state.wait_for and state.wait_for.player == player.name:
                if state.wait_for.type == InputType.ACTION:
                    asyncio.create_task(input_direction())
                elif state.wait_for.type == InputType.POWER_UP:
                    asyncio.create_task(input_select())
            else:
                render_game(game.get_state())

        game.add_output_listener(output_listener)
        print('Start Test Game')
        render_game(game.get_state())
        asyncio.run(game.run())


if __name__ == "__main__":
    main()
