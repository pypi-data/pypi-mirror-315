import os
import unittest

import potx

from potx.api.ocr import SmartStructuralOCRV2


class TestTencent(unittest.TestCase):

    def setUp(self):
        self.SecretId = os.getenv("SecretId", None)
        self.SecretKey = os.getenv("SecretKey", None)

        self.ak = os.getenv('ak', None)
        self.sk = os.getenv('sk', None)

    def test_SmartStructuralOCRV2(self):
        r = SmartStructuralOCRV2(id=self.SecretId, key=self.SecretKey,
                                 img_path=r'./test_files/程序员晚枫的手写发票.png')
        print(r)
    def test_doc(self):
        print(potx.__doc__)