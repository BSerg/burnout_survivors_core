import asyncio
import random

from components.ai_component import AiComponent
from components.initiative_component import InitiativeComponent
from factories.enemy_factory import create_enemy
from factories.game_factory import create_game
from models.enemy_model import EnemyConfig
from models.game_model import GameConfig, GameModel
from models.input_model import Direction, InputModel
from models.melee_weapon_model import MeleeWeaponConfig
from models.player_model import PlayerConfig
from models.shared import Point
from utils.utils import async_input

test_config: GameConfig = GameConfig(
    seed='test',
    players=[
        PlayerConfig(
            name='player',
            position=Point(x=0, y=0),
            health=100,
            initiative=1,
            weapon=MeleeWeaponConfig(type='sword', damage=5)
        )
    ]
)

test_enemy_config: EnemyConfig = EnemyConfig(
    name='enemy',
    position=Point(x=0, y=0),
    health=10,
    tags=set(['enemy']),
    weapon=MeleeWeaponConfig(type='teeth', damage=10),
    initiative=0.75
)

state = {}
grass = [Point(x=random.randint(-50, 50), y=random.randint(-50, 50))
         for _ in range(200)]


def render_game(state: GameModel):
    radius = 5

    if state.players and len(state.players):
        player = state.players[0]
        enemies = state.enemies or list()

        print(f'\rPlayer: {player.health}HP')

        for k in range(player.position.y - radius, player.position.y + radius + 1):
            row = []
            for i in range(player.position.x - radius, player.position.x + radius + 1):
                if (i == player.position.x and k == player.position.y):
                    if player.status == 'damaged':
                        row.append('x')
                    else:
                        row.append('p')
                else:
                    for enemy in [e for e in enemies if e.health > 0]:
                        if i == enemy.position.x and k == enemy.position.y:
                            if enemy.status == 'damaged':
                                row.append('x')
                            else:    
                                row.append('e')
                            break
                    else:
                        for g in grass:
                            if g.x == i and g.y == k:
                                row.append('~')
                                break
                        else:
                            row.append('-')
            print(' '.join(row))


def merge_state(state: GameModel, new_state: GameModel):
    players = new_state.players or list()
    players_names = [p.name for p in players]

    for p in state.players or list():
        if p.name not in players_names:
            players.append(p)

    enemies = new_state.enemies or list()
    enemies_names = [p.name for p in enemies]

    for p in state.enemies or list():
        if p.name not in enemies_names:
            enemies.append(p)

    state.players = players
    state.enemies = enemies
    state.wait_for = new_state.wait_for

    return state


def main():
    game = create_game(test_config)

    player = list(game.objects.findByTag('player'))[0]

    for i in range(3):
        config = test_enemy_config.model_copy()
        config.name += f'_{i}'
        config.position = Point(x=random.randint(-5, 5),
                                y=random.randint(-5, 5))
        enemy = create_enemy(game, config)
        enemy.requireComponent(
            InitiativeComponent).initiative_accumulator = random.random()
        enemy.requireComponent(AiComponent).target = player
        game.objects.add(enemy)

    _state: GameModel = game.get_state(updated_only=False)

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
            asyncio.create_task(input_direction())
        else:
            merge_state(_state, state)
            render_game(_state)

    game.on_output(output_listener)

    print('Start Test Game')

    asyncio.run(game.run())


if __name__ == "__main__":
    main()
