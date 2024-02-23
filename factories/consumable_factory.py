from game import Game
from models.consumable_model import ConsumableConfig
from objects.consumable.consumable import Consumable
from objects.consumable.exp_consumable import ExpConsumable
from objects.consumable.health_consumable import HealthConsumable
from utils.utils import get_uuid


def create_consumable(game: Game, config: ConsumableConfig) -> Consumable:
    if config.type == 'exp':
        return ExpConsumable(f'exp_{get_uuid()}', game, config.value)

    if config.type == 'health':
        return HealthConsumable(f'health_{get_uuid()}', game, config.value)

    raise Exception('Consumable type not found')
