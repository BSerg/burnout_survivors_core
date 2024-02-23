from objects.game_object import GameObject


class Upgrade(GameObject):
    def modify(self, value):
        return value

    def get_state(self) -> None:
        return None
