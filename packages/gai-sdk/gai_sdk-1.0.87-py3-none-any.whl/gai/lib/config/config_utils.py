import os
import yaml
from gai.lib.common.utils import get_app_path

def get_gai_config(file_path=None):
    app_dir=get_app_path()
    global_lib_config_path = os.path.join(app_dir, 'gai.yml')
    if file_path:
        global_lib_config_path = file_path
    with open(global_lib_config_path, 'r') as f:
        return yaml.load(f, Loader=yaml.FullLoader)
    
def save_gai_config(config, file_path=None):
    app_dir=get_app_path()
    global_lib_config_path = os.path.join(app_dir, 'gai.yml')
    if file_path:
        global_lib_config_path = file_path
    with open(global_lib_config_path, 'w') as f:
        yaml.dump(config, f, sort_keys=False)
    
def get_gai_url(category_name):
    config = get_gai_config()
    key = f"gai-{category_name}"
    url = config["clients"][key]["url"]
    return url

# "api_url" property contains the fully qualified domain name of this API server
def get_api_url():
    config = get_gai_config()
    url = config["api_url"]
    return url

CONFIG = None
try:
    CONFIG = get_gai_config()
except Exception as e:
    pass

TTT_CONFIG = None if not CONFIG else CONFIG["clients"]["gai-ttt"]
RAG_CONFIG = None if not CONFIG else CONFIG["clients"]["gai-rag"]
TTI_CONFIG = None if not CONFIG else CONFIG["clients"]["gai-tti"]
ITT_CONFIG = None if not CONFIG else CONFIG["clients"]["gai-itt"]
STT_CONFIG = None if not CONFIG else CONFIG["clients"]["gai-stt"]
TTS_CONFIG = None if not CONFIG else CONFIG["clients"]["gai-tts"]
