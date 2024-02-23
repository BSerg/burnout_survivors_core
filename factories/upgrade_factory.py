from models.update_model import ExpUpdateConfig, HealthUpdateConfig
from objects.upgrades.upgrade import Upgrade
from game import Game
from objects.upgrades.health_upgrade import HealthUpgrade

UpgradeConfig = HealthUpdateConfig | ExpUpdateConfig


def create_upgrade(game: Game, config: UpgradeConfig) -> HealthUpgrade:
    if isinstance(config, HealthUpdateConfig):
        return HealthUpgrade(game, config.health_modificator)

    raise Exception('Upgrade config is unknown')
