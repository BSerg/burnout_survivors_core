from components.component import Component
from objects.game_object import GameObject
from components.status_component import Status, StatusComponent


class VitalityComponent(Component):
    def __init__(self, game_object: GameObject, health: float = 1) -> None:
        super().__init__('vitality_component', game_object)
        self._health = health
        self._max_health = health

    @property
    def health(self) -> float:
        return self._health
    
    @health.setter
    def health(self, value: float) -> None:
        self._health = value

    @property
    def max_health(self) -> float:
        return self._max_health
    
    @max_health.setter
    def max_health(self, value: float) -> None:
        self._max_health = value
        
    @property
    def is_dead(self) -> bool:
        return self._health <= 0

    def heal(self, value: float) -> None:
        self._health = min(self._health + value, self._max_health)
        self._game_object.updated = True

    def damage(self, value: float) -> None:
        self._health = max(self._health - value, 0)
        
        self._game_object.updated = True
        
        status_component = self._game_object.findComponent(StatusComponent)
        if status_component:
            status_component.status = Status.DAMAGED.value
    
        if self._health > 0:
            self._game_object.game.log(f'{self._game_object.name} got damage {value}HP')
        else:
            self._game_object.game.log(f'{self._game_object.name} is dead')
            

    def increase_max_health(self, value: float) -> None:
        self._max_health += value
