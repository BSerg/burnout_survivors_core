import asyncio
import random

from components.ai_component import AiComponent
from components.initiative_component import InitiativeComponent
from components.vitality_component import VitalityComponent
from factories.enemy_factory import create_enemy
from factories.game_factory import create_game
from models.consumable_model import ConsumableConfig
from models.enemy_model import EnemyConfig
from models.game_model import GameConfig, GameModel, InputType
from models.input_model import Direction, InputModel
from models.melee_weapon_model import MeleeWeaponConfig
from models.player_model import PlayerConfig
from models.shared import PointModel
from utils.utils import async_input, get_uuid
from game_manager import GameManager
from game_context import GameContext

test_config: GameConfig = GameConfig(
    seed='test',
    players=[
        PlayerConfig(
            name='Player',
            position=PointModel(x=0, y=0),
            health=100,
            vision_radius=5,
            exp_consume_radius=1,
            weapon=MeleeWeaponConfig(type='sword', damage=5),
            upgrades=[]
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
                value=1
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

        print(f'\rPlayer: {player.health}HP')

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

        async def input_direction():
            value = await async_input('Enter direction (left, up, right, down): ')
            try:
                game.send_to_input(InputModel(
                    player_name=player.name, direction=Direction(value)))
            except:
                game.send_to_input(InputModel(
                    player_name=player.name, direction=None))

        def output_listener(state: GameModel):
            if state.wait_for and state.wait_for.player == player.name:
                if state.wait_for.type == InputType.ACTION:
                    asyncio.create_task(input_direction())
            else:
                render_game(game.get_state())

        game.add_output_listener(output_listener)
        print('Start Test Game')
        render_game(game.get_state())
        asyncio.run(game.run())


if __name__ == "__main__":
    main()
