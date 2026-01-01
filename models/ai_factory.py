from models.ai import Ai


class AiFactory:
    @staticmethod
    def get_ai(depth: int) -> Ai:
        return Ai(depth)
