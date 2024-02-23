from components.initiative_component import InitiativeComponent
from components.melee_component import MeleeComponent
from components.position_component import PositionComponent
from components.vitality_component import VitalityComponent
from factories.weapon_factory import create_weapon
from game import Game
from models.enemy_model import EnemyConfig
from objects.enemy import Enemy
from factories.consumable_factory import create_consumable
from components.drop_component import DropComponent
from utils.game import Point


def create_enemy(game: Game, config: EnemyConfig) -> Enemy:
    enemy = Enemy(config.name, game)

    # POSITION
    enemy.require_component(PositionComponent).position = Point(
        x=config.position.x, y=config.position.y)

    # VITALITY
    vitality_component = enemy.require_component(VitalityComponent)
    vitality_component.health = config.health
    vitality_component.max_health = config.health

    # INITIATIVE
    enemy.require_component(InitiativeComponent).initiative = config.initiative

    # WEAPON
    weapon = create_weapon(enemy, config.weapon)
    weapon.owner = enemy
    enemy.require_component(MeleeComponent).weapon = weapon

    # DROP
    if config.drop_object:
        drop_object = create_consumable(game, config.drop_object)
        enemy.require_component(DropComponent).drop_object = drop_object

    return enemy
