from components.experience_component import ExperienceComponent
from components.initiative_component import InitiativeComponent
from components.melee_component import MeleeComponent
from components.position_component import PositionComponent
from components.vitality_component import VitalityComponent
from game import Game
from models.player_model import PlayerConfig
from objects.player import Player
from factories.weapon_factory import create_weapon


def create_player(game: Game, config: PlayerConfig) -> Player:
    player = Player(config.name, game)

    # POSITION
    player.require_component(PositionComponent).position = config.position

    # VITALITY
    vitality_component = player.require_component(VitalityComponent)
    vitality_component.health = config.health
    vitality_component.max_health = config.health

    # INITIATIVE
    player.require_component(
        InitiativeComponent).initiative = config.initiative

    # WEAPON
    weapon = create_weapon(player, config.weapon)
    weapon.owner = player
    player.require_component(MeleeComponent).weapon = weapon

    return player
