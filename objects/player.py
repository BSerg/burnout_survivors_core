from __future__ import annotations

from typing import TYPE_CHECKING

from components.experience_component import ExperienceComponent
from components.melee_component import MeleeComponent
from components.move_component import MoveComponent
from components.player_component import PlayerComponent
from components.position_component import PositionComponent
from components.status_component import StatusComponent
from components.vision_component import VisionComponent
from components.vitality_component import VitalityComponent
from models.player_model import PlayerModel
from objects.game_object import GameObject
from upgrades.upgrade_manager import UpgradeManager

if TYPE_CHECKING:
    from game import Game


class Player(GameObject[PlayerModel]):
    def __init__(self, name: str, game: Game) -> None:
        super().__init__(name, game, tags=set(['player']))

        self._components = [
            StatusComponent(self),
            PositionComponent(self),
            MoveComponent(self),
            VitalityComponent(self),
            VisionComponent(self),
            ExperienceComponent(self),
            MeleeComponent(self),
            PlayerComponent(self),
        ]

        self._upgrade_manager = UpgradeManager()

    @property
    def upgrades(self) -> UpgradeManager:
        return self._upgrade_manager

    def get_state(self) -> PlayerModel:
        position_component = self.require_component(
            PositionComponent)
        vitality_component = self.require_component(VitalityComponent)
        exp_component = self.require_component(ExperienceComponent)
        vision_component = self.require_component(VisionComponent)
        status_component = self.require_component(StatusComponent)
        return PlayerModel(
            name=self.name,
            tags=self.tags,
            position=position_component.position.get_state(),
            health=vitality_component.health,
            max_health=vitality_component.max_health,
            vision_radius=vision_component.radius,
            experience=exp_component.exp,
            level=exp_component.level,
            status=status_component.status
        )
