# python -m ALGSFan.Tests.UnitTest

from .TestALGSSheet import TestALGSSheet
from .TestLiquipedia import TestLiquipedia
from .TestTWSCCalendar import TestTWSCCalendar
from ALGSFan.Utils import set_logger

def main():
    set_logger('Logs/test.log')
    TestALGSSheet()
    TestLiquipedia()
    TestTWSCCalendar()

if __name__ == '__main__':
    main()
