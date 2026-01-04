from models.bot import Bot


class BotFactory:
    @staticmethod
    def get_bot(depth: int) -> Bot:
        return Bot(depth)
