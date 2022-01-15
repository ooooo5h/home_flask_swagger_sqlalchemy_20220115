"""
Flask Configuration
"""

class Config(object):
    DEBUG = False
    TESTING = False
    
    
class ProductionConfig(Config):
    pass

class TestConfig(Config):
    TESTING = True
    
class DebugConfig(Config):
    DEBUG = True