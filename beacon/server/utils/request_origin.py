from server.config import config

def check_request_origin():
    #project_instance = "generic"
    project_instance = config.project_instance 
    return project_instance
