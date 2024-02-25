from game import Game
from models.consumable_model import ConsumableConfig
from objects.consumables.consumable import Consumable
from objects.consumables.exp_consumable import ExpConsumable
from objects.consumables.health_consumable import HealthConsumable
from utils.utils import get_uuid


def create_consumable(config: ConsumableConfig) -> Consumable:
    if config.type == 'exp':
        return ExpConsumable(f'exp_{get_uuid()}', config.value)

    if config.type == 'health':
        return HealthConsumable(f'health_{get_uuid()}', config.value)

    raise Exception('Consumable type not found')
