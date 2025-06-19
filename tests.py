import unittest

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file


class TestGetFilesInfo(unittest.TestCase):
    def test_calculator_info_current(self):
        result = get_files_info("calculator", ".")
        print(result)

    def test_calculator_info_pkg(self):
        result = get_files_info("calculator", "pkg")
        print(result)

    def test_calculator_info_bin(self):
        result = get_files_info("calculator", "/bin")
        print(result)
        self.assertTrue(result.startswith("Error: "))

    def test_calculator_info_up(self):
        result = get_files_info("calculator", "../")
        print(result)
        self.assertTrue(result.startswith("Error: "))


class TestGetFilesContent(unittest.TestCase):
    def test_calculator_content_main(self):
        result = get_file_content("calculator", "main.py")
        print(result)

    def test_calculator_content_pkg(self):
        result = get_file_content("calculator", "pkg/calculator.py")
        print(result)

    def test_calculator_content_bin(self):
        result = get_file_content("calculator", "/bin/cat")
        print(result)


class TestWriteFile(unittest.TestCase):
    def test_calculator_write_main(self):
        result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        print(result)

    def test_calculator_write_pkg(self):
        result = write_file(
            "calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"
        )
        print(result)

    def test_calculator_write_tmp(self):
        result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        print(result)


if __name__ == "__main__":
    unittest.main()
