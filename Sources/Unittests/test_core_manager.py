import os
import unittest

from Core import config_manager as cm
from manager import Manager
from Core.ffgl_parameter import FFGLParameter

class MyTestCase(unittest.TestCase):
    def test_simple_FFGL_one_parameter(self):
        # self.assertEqual(True, False)
        config_datas = cm.get_datas()
        self.ffgl_manager = Manager(config_datas)
        p = FFGLParameter("FF_TYPE_STANDARD", True, "abc", "1.0", 0)
        parameters = [p]
        self.ffgl_manager.CreateFFGL("2", "FX", parameters, "test1",
                                     "test", "MirrorStripes", shader_code="")

    def test_simple_FFGL_two_parameter(self):
        #self.assertEqual(True, False)
        config_datas = cm.get_datas()
        self.ffgl_manager = Manager(config_datas)
        p = FFGLParameter("FF_TYPE_STANDARD", True, "ptest1", "1.0", 0)
        p2 = FFGLParameter("FF_TYPE_STANDARD", True, "ptest2", "1.0", 1)
        parameters = [p,p2]
        self.ffgl_manager.CreateFFGL("2", "FX", parameters, "test1",
                                     "test", "TestName", shader_code="")

    def test_simple_FFGL_no_parameter(self):
        #self.assertEqual(True, False)
        config_datas = cm.get_datas()
        self.ffgl_manager = Manager(config_datas)
        parameters = []
        self.ffgl_manager.CreateFFGL("2", "FX", parameters, "test1",
                                     "test", "MirrorStripes")

if __name__ == '__main__':
    unittest.main()
