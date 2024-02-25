from models.upgrade_model import *
from objects.upgrades.upgrade import Upgrade
from game import Game
from objects.upgrades.health_upgrade import HealRateUpgrade, HealthUpgrade
from objects.player import Player


def create_upgrade(player: Player, config: UpgradeConfig) -> Upgrade:
    if isinstance(config, HealthUpgradeConfig):
        return HealthUpgrade(config.name, player, config.value)

    if isinstance(config, HealRateUpgradeConfig):
        return HealRateUpgrade(config.name, player, config.value)

    if isinstance(config, ExpConsumeRadiusUpgradeConfig):
        pass

    if isinstance(config, ExpConsumeRateUpgradeConfig):
        pass

    raise Exception('Upgrade config is unknown')
