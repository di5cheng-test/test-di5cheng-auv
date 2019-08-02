import pytest
import time
import sys
import os
from src.common import send_email

global null
null = None

if __name__ == "__main__":
    sys.path.append(os.path.split(os.path.realpath(__file__))[0])
    # report_path = '--html=./report/html/' + 'report_' + str(int(time.time())) + '.html'
    # pytest.main(['-s', '-q', '--tb=no', report_path])
    # send_email.send_email().sendReport()
    pytest.main(["-s", "-q", "--alluredir", "C:/Program Files (x86)/Jenkins/workspace/auv_test_report"])
    # os.system("allure generate report/ -o report/html")
