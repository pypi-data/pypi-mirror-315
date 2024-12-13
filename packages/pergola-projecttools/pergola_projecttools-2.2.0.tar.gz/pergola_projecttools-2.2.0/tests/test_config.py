import pytest
from src.pergolaprojecttools.config_util import ConfigUtilBase
from src.pergolaprojecttools.exceptions import ConfigException

class NoFileConfigUtil(ConfigUtilBase):
    pass

class TestConfigUtil(ConfigUtilBase):

    config_path = 'tests/config/config.json'

    def get_batman(cls):
        return cls.get_config_value('batman')

    def get_batmans_car(cls):
        return cls.get_inner_value(cls.get_config_value('batmandetails'), 'preferredVehicle')

class ReadmeConfigUtil(ConfigUtilBase):
    import pathlib
    config_path = f"{pathlib.Path(__file__).parent}/config/config-readme.json"

    @classmethod
    def get_user(cls) -> str:
        return cls.get_config_value('username')

    @classmethod
    def get_appearance(cls) -> dict:
        return cls.get_config_value('appearance')

    @classmethod
    def get_theme(cls) -> str:
        return cls.get_inner_value(cls.get_config_value('appearance'), 'theme')

    @classmethod
    def get_size(cls) -> int:
        return cls.get_inner_value(cls.get_config_value('appearance'), 'size')


def test_no_config_file():
    config_util = NoFileConfigUtil()
    with pytest.raises(ConfigException) as excinfo:
        config_util.get_config_value('something')

    assert "ConfigUtilBase.config_path" in str(excinfo.value)

def test_get_config_inner():
    config_util = TestConfigUtil()

    batman = config_util.get_batmans_car()
    assert batman == "bat mobile"

def test_get_config():
    config_util = TestConfigUtil()

    batman = config_util.get_batman()
    assert batman == "Bruce Wayne"

def test_readme_1():
    ConfigUtilBase.config_path = 'tests/config/config-readme.json'

    assert ConfigUtilBase.get_config_value("username") == 'John'

def test_readme_2():
    assert ReadmeConfigUtil.get_size() == 500