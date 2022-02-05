from ALGSFan import LiquipediaSearchNextMatch
from loguru import logger


def TestLiquipedia():
    logger.info(LiquipediaSearchNextMatch("nice"))
    logger.info(LiquipediaSearchNextMatch("has"))
    logger.info(LiquipediaSearchNextMatch("rex"))
    logger.info(LiquipediaSearchNextMatch("classic"))


if __name__ == "__main__":
    TestLiquipedia()
