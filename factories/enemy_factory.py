from components.initiative_component import InitiativeComponent
from components.melee_component import MeleeComponent
from components.position_component import PositionComponent
from components.vitality_component import VitalityComponent
from factories.weapon_factory import create_weapon
from game import Game
from models.enemy_model import EnemyConfig
from objects.enemy import Enemy


def create_enemy(game: Game, config: EnemyConfig) -> Enemy:
    enemy = Enemy(config.name, game)

    # POSITION
    enemy.requireComponent(PositionComponent).position = config.position

    # VITALITY
    vitality_component = enemy.requireComponent(VitalityComponent)
    vitality_component.health = config.health
    vitality_component.max_health = config.health

    # INITIATIVE
    enemy.requireComponent(InitiativeComponent).initiative = config.initiative

    # WEAPON
    weapon = create_weapon(enemy, config.weapon)
    weapon.owner = enemy
    enemy.requireComponent(MeleeComponent).weapon = weapon

    return enemy
