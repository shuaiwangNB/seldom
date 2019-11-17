import os
import sys
import argparse
import logging
from pyse import __description__, __version__

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

PY3 = sys.version_info[0] == 3


def main():
    """ API test: parse command line options and run commands.
    """

    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument(
        '-V', '--version', dest='version', action='store_true',
        help="show version")

    parser.add_argument(
        '--startproject',
        help="Specify new project name.")

    parser.add_argument(
        '-r',
        help="run test case")

    args = parser.parse_args()

    if args.version:
        print("version {}".format(__version__), )
        return 0

    project_name = args.startproject
    if project_name:
        create_scaffold(project_name)
        return 0

    run_file = args.r
    if run_file:
        if PY3:
            py_version = "python3 -V"
            os.system(py_version)
            command = "python3 " + run_file
        else:
            py_version = "python -V"
            os.system(py_version)
            command = "python " + run_file
        os.system(command)
        return 0


def create_scaffold(project_name):
    """ create scaffold with specified project name.
    """
    if os.path.isdir(project_name):
        logger.info(u"Folder {} exists, please specify a new folder name.".format(project_name))
        return

    logger.info("Start to create new test project: {}".format(project_name))
    logger.info("CWD: {}\n".format(os.getcwd()))

    def create_folder(path):
        os.makedirs(path)
        msg = "created folder: {}".format(path)
        logger.info(msg)

    def create_file(path, file_content=""):
        with open(path, 'w') as f:
            f.write(file_content)
        msg = "created file: {}".format(path)
        logger.info(msg)

    sample_page = '''from poium import Page, PageElement


class BaiduPage(Page):
    """baidu page element"""
    search_input = PageElement(id_="kw")
    search_button = PageElement(id_="su")

'''
    test_sample = '''import pyse
from page.sample_page import BaiduPage


class YouTest(pyse.TestCase):

    def test_case(self):
        """a simple test case """
        page = BaiduPage(self.driver)
        page.get("https://www.baidu.com")
        page.search_input = "pyse"
        page.search_button.click()
        self.assertTitle("pyse")

'''
    run_test = """import pyse


if __name__ == '__main__':
    # run test
    # pyse.main("./test_dir/")
    pyse.main("./test_dir/test_sample.py")

"""
    create_folder(project_name)
    create_folder(os.path.join(project_name, "page"))
    create_folder(os.path.join(project_name, "test_dir"))
    create_folder(os.path.join(project_name, "reports"))
    create_file(os.path.join(project_name, "page", "sample_page.py"), sample_page)
    create_file(os.path.join(project_name, "test_dir", "test_sample.py"), test_sample)
    create_file(os.path.join(project_name, "run.py"), run_test)

