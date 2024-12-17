from unittest import TestCase

from my_package.hello import hello1


class Test(TestCase):
    def test_hello1(self):
        assert hello1() == "hello world"
