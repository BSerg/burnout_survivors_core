from models.upgrade_model import *
from objects.upgrades.upgrade import Upgrade
from game import Game
from objects.upgrades.health_upgrade import HealRateUpgrade, HealthUpgrade
from objects.player import Player
from objects.upgrades.exp_upgrade import ExpConsumeRadiusUpgrade, ExpConsumeRateUpgrade


def create_upgrade(player: Player, parent: Upgrade | None, config: UpgradeConfig) -> Upgrade:
    upgrade: Upgrade | None = None

    if isinstance(config, HealthUpgradeConfig):
        upgrade = HealthUpgrade(config.name, player, parent, config.value)

    if isinstance(config, HealRateUpgradeConfig):
        upgrade = HealRateUpgrade(config.name, player, parent, config.value)

    if isinstance(config, ExpConsumeRadiusUpgradeConfig):
        upgrade = ExpConsumeRadiusUpgrade(config.name, player, parent, config.value)

    if isinstance(config, ExpConsumeRateUpgradeConfig):
        upgrade = ExpConsumeRateUpgrade(config.name, player, parent, config.value)

    if upgrade:
        for next_config in config.next_upgrades:
            upgrade.add(create_upgrade(player, upgrade, next_config))
        return upgrade

    raise Exception('Upgrade config is unknown')
