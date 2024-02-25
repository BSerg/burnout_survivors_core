from components.experience_component import ExperienceComponent
from components.melee_component import MeleeComponent
from components.position_component import PositionComponent
from components.vitality_component import VitalityComponent
from factories.weapon_factory import create_weapon
from models.player_model import PlayerConfig
from objects.player import Player
from utils.game import Point


def create_player(config: PlayerConfig) -> Player:
    player = Player(config.name)

    # POSITION
    player.require_component(PositionComponent).position = Point(
        x=config.position.x, y=config.position.y)

    # VITALITY
    vitality_component = player.require_component(VitalityComponent)
    vitality_component.health = config.health
    vitality_component.max_health = config.health

    # EXPIRIENCE
    exp_component = player.require_component(ExperienceComponent)
    exp_component.consume_radius = config.exp_consume_radius

    # WEAPON
    weapon = create_weapon(player, config.weapon)
    weapon.owner = player
    player.require_component(MeleeComponent).weapon = weapon

    return player
