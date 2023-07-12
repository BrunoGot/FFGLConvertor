import json

#config
def get_datas():
    """
    load the current json config and return the parsed datas
    :return dic: config_data from parsed json
    """
    config_file_path = "D:\Documents\Code\Python\FFGLConvertor\Sources\config.json"
    with open(config_file_path) as json_file:
        config_file = json_file.read()
    config_data = json.loads(config_file)
    return config_data