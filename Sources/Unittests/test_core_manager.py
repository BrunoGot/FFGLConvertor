import os
import unittest

from Core import config_manager as cm
from Core.ffgl_parameter import FFGLParameter
from manager import Manager
from UI.main_window import FFGL_write_window

class MyTestCase(unittest.TestCase):
    def test_simple_FFGL_one_parameter(self):
        # self.assertEqual(True, False)
        config_datas = cm.get_datas()
        self.ffgl_manager = Manager(config_datas)
        p = FFGLParameter("FF_TYPE_STANDARD", True, "Abc", "1.0", 0)
        parameters = [p]
        sources_path = self.ffgl_manager.CreateFFGL("2", "FX", parameters, "test1",
                                     "test", "MirrorStripes", shader_code="",pluginId="132e")
        self.assertTrue(os.path.exists(sources_path["cpp"]))
        self.assertTrue(os.path.exists(sources_path["header"]))
        with open(sources_path["cpp"],"r") as file:
            txt = file.read()
            self.assertIn('SetParamInfof(FFPARAM_1, "Abc", FF_TYPE_STANDARD);',txt)
            self.assertIn('m_paramAbc(1.0 ),',txt)
            self.assertIn('#define FFPARAM_1 (0)',txt)
            self.assertIn('ParamLocation1= m_shader.FindUniform("m_param1_1");',txt)
            self.assertIn('m_paramAbc = value;',txt)
            self.assertIn('return m_paramAbc;',txt)

    def test_simple_FFGL_two_parameter(self):
        #self.assertEqual(True, False)
        config_datas = cm.get_datas()
        self.ffgl_manager = Manager(config_datas)
        p = FFGLParameter("FF_TYPE_STANDARD", True, "ptest1", "1.0", 0)
        p2 = FFGLParameter("FF_TYPE_STANDARD", True, "ptest2", "1.0", 1)
        parameters = [p,p2]
        self.ffgl_manager.CreateFFGL("2", "FX", parameters, "test1",
                                     "test", "TestName", shader_code="",pluginId="132e")

    def test_simple_FFGL_no_parameter(self):
        #self.assertEqual(True, False)
        config_datas = cm.get_datas()
        self.ffgl_manager = Manager(config_datas)
        parameters = []
        self.ffgl_manager.CreateFFGL("2", "FX", parameters, "test1",
                                     "test", "MirrorStripes", shader_code="",pluginId="132e")

    def test_simple_FFGL_export(self):
        """
        test a simple ffgl export on a c++ solution
        """
        config_datas = cm.get_datas()
        self.ffgl_manager = Manager(config_datas)
        ffgl_name = "TestName"
        cpp_path_project = os.path.join(config_datas["FFGLSolutionPath"], f"{ffgl_name}.vcxproj")
        if os.path.isfile(cpp_path_project):
            os.remove(cpp_path_project)
        #check that the path doesn't exist before exporting
        self.assertFalse(os.path.isfile(cpp_path_project))
        self.ffgl_manager.export_ffgl(ffgl_name)
        self.assertTrue(os.path.isfile(cpp_path_project))


    # def test_loading_parameter(self):
    #     ffgl_win = FFGL_write_window()
    #     path = "D:\Documents\Code\Python\FFGLConvertor\Sources\TestShaders\TestParam1.shd"
    #     f = open(path, "r")
    #     datas = f.read().split(self.shader_file_spliter)
    #     ffgl_win.load_datas(datas)
    #     print(ffgl_win.parameters)
    #     f.close()
if __name__ == '__main__':
    unittest.main()
