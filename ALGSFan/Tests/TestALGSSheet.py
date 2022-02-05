from ALGSFan import ALGSSheet
from loguru import logger


def TestALGSSheet():
    sheet_nice = ALGSSheet(0, 456357272, "Nice")
    sheet_rex = ALGSSheet(286280759, 2078813387, "Rex")
    sheet_algs = ALGSSheet(848841058, 1658593575, "ALGS")

    def test(msg, sheet: ALGSSheet):
        logger.info(msg)
        for _ in range(10):
            logger.info(sheet.get_msg())

    test("Nice Sheet", sheet_nice)
    test("Rex Sheet", sheet_rex)
    test("ALGS Sheet", sheet_algs)


if __name__ == "__main__":
    TestALGSSheet()
