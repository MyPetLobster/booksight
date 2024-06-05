class VisionConfig:
    def __init__(self, email, formats, ai_model, ai_temp, torch_confidence, api_keys):
        self.email = email
        self.formats = formats
        self.ai_model = ai_model
        self.ai_temp = ai_temp
        self.torch_confidence = torch_confidence
        self.api_keys = api_keys  # Dictionary of API keys

# Global variable to hold the configuration
global_config = None

def set_config(config):
    global global_config
    global_config = config

def get_config():
    return global_config