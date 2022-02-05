from ALGSFan import TWSCCalendar
from loguru import logger


def TestTWSCCalendar():
    tc = TWSCCalendar()

    logger.info(f"TWSCCalendar().get_next_event(): {tc.get_next_event()}")
    logger.info(
        f"TWSCCalendar().get_next_event(next_only=True): "
        f"{tc.get_next_event(next_only=True)}"
    )
    logger.info(f"TWSCCalendar().get_next_sign(): {tc.get_next_sign()}")


if __name__ == "__main__":
    TestTWSCCalendar()
