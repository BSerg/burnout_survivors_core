from __future__ import annotations

from typing import TYPE_CHECKING

from components.experience_component import ExperienceComponent
from components.initiative_component import InitiativeComponent
from components.melee_component import MeleeComponent
from components.move_component import MoveComponent
from components.position_component import PositionComponent
from components.status_component import StatusComponent
from components.vitality_component import VitalityComponent
from models.player_model import PlayerModel
from objects.game_object import GameObject
from components.player_input_component import PlayerInputComponent

if TYPE_CHECKING:
    from game import Game


class Player(GameObject[PlayerModel]):
    def __init__(self, name: str, game: Game) -> None:
        super().__init__(name, game, tags=set(['player']))

        self._components = [
            PlayerInputComponent(self),
            StatusComponent(self),
            InitiativeComponent(self),
            PositionComponent(self),
            MoveComponent(self),
            VitalityComponent(self),
            ExperienceComponent(self),
            MeleeComponent(self),
        ]

    def get_state(self) -> PlayerModel:
        position_component = self.requireComponent(PositionComponent)
        vitality_component = self.requireComponent(VitalityComponent)
        exp_component = self.requireComponent(ExperienceComponent)
        status_component = self.requireComponent(StatusComponent)
        return PlayerModel(
            name=self.name,
            tags=self.tags,
            position=position_component.position,
            health=vitality_component.health,
            max_health=vitality_component.max_health,
            experience=exp_component.exp,
            level=exp_component.level,
            status=status_component.status
        )