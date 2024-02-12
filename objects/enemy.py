from components.ai_component import AiComponent
from components.initiative_component import InitiativeComponent
from components.melee_component import MeleeComponent
from components.move_component import MoveComponent
from components.position_component import PositionComponent
from components.status_component import StatusComponent
from components.vitality_component import VitalityComponent
from game import Game
from models.enemy_model import EnemyModel
from objects.game_object import GameObject


class Enemy(GameObject[EnemyModel]):
    def __init__(self, name: str, game: Game) -> None:
        super().__init__(name, game, set(['enemy']), [
            StatusComponent(self),
            InitiativeComponent(self),
            PositionComponent(self),
            MoveComponent(self),
            VitalityComponent(self),
            MeleeComponent(self),
            AiComponent(self)
        ])

    def get_state(self) -> EnemyModel:
        position_component = self.require_component(PositionComponent)
        vitality_component = self.require_component(VitalityComponent)
        status_component = self.require_component(StatusComponent)
        return EnemyModel(
            name=self.name,
            tags=self.tags,
            position=position_component.position,
            health=vitality_component.health,
            max_health=vitality_component.max_health,
            status=status_component.status
        )
