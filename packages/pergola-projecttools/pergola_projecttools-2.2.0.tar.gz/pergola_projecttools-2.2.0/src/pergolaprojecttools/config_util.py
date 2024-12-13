from os import getcwd
import json

from argparse import Namespace

from .exceptions import ConfigException

class ConfigUtilBase:
    """
    Wrapper for a JSON file, holding application configuration provided by Pergola. See [Pergola Configuration Management](https://docs.pergola.cloud/docs/reference/configurations) for details on the concept.

    Usage:
    1) At first, in your application, provide a path for config-files. Create a subdirectory named config and make sure it gets pushed to git (or your VCS provider). This can e.g. be enforced by adding a .gitignore file with the this content there:
    ```
    *.json
    !config.template.json
    ```
    Note, that this has the additional benefit of never accidentally commiting any json config files with passwords or other secrets.
    2) Put a file called config.json into the config subdirectory. Add some config values into the file, e.g.
    ```
    {
      "username": "John",
      "appearance": {
          "theme": "dark",
          "size": 500
      }
    }
    ```

    3) Use ConfigUtil to access your config utils, either quick or more sophisticated
        a) the quick and simple method:
        ```
        from pergolaprojecttools.config_util import ConfigUtilBase

        # Use it right away
        ConfigUtilBase.get_config_value("username") # returns 'John'
        ConfigUtilBase.get_config_value("appearance") # returns a dict with 'theme' and 'size'
        ```
        b) the sophisticated method
        Create a class ConfigUtil inheriting from ConfigUtilBase and add get methods for all your config parameters, ensuring a safe usage.
        This approach also gives you more control, e.g. to specify the config file path or to navigate deeper into your JSON structure. For our example, this could look like:
        ```
class ConfigUtil(ConfigUtilBase):

    config_path = f"{os.getcwd()}/config/config.json"

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
        ```

        Your own ConfigUtil class can be used directly like:
        ```
        the_user_name = ConfigUtil.get_user()
        ```

    4) Try this out locally, it works during development, in IDEs like Visual Studio or toolings like Jupyter
    5) To provide configurations in Pergola, got to the Config Management of a Pergola stage. Create a file called my-stage-config.json (named appropriately for your purpose).
    6) Bring it together by mapping the file in pergola.yaml:
       ```
components:
  - name: my-component-name
[...]
    files:
      - path: /app/config/config.json
        config-ref: my-stage-config.json
[...]
       ```

       A few notes here:
       - projecttools ConfigUtilBase class uses a default path for its config file of  <application-root>/config/config.json
       - Thus, the example above assumes the python application to be located in /app
       - config-ref, defined as my-stage-config.json is the name of the file in the Pergola stage config. The application will never see this file name, it will be mapped to /app/config/config.json
       - See [Pergola Manifest Reference](https://docs.pergola.cloud/docs/reference/project-manifest) for details.
    3) In your application, create a subdirectory config and make sure it gets pushed to git (or your VCS provider). This can e.g. be enforced by adding a .gitignore file with the this content there:
    ```
    *.json
    !config.template.json
    ```
    Note, that this has the additional benefit of never accidentally commiting any json config files with passwords or other secrets.

    And never forget: Do not put passwords or other secrets into your source code, always use a secure Pergola config!

    """

    config_path: str = f"{getcwd()}/config/config.json"
    key_argoverrides: str = "argoverrides"

    config_content: dict = None

    @classmethod
    def get_config_value(cls, key: str, default_value = None):
        """Get a config value

        Args:
            key (str): The key whose value is to be retrieved
            default_value(mixed): OPTIONAL default value if key is not found.

        If no default_value is given and the key is not found --> Exception

        Returns:
            Any: Any type of content stored, configured at the location of the key
        """
        if cls.config_content is None:
            cls._init_config_data()

        if key in cls.config_content:
            return cls.config_content[key]
        else:
            if default_value is not None:
                return default_value
            else:
                raise Exception(f"[ConfigError] key '{key}' not found in config file '{cls.config_path}'")


    @classmethod
    def get_inner_value(cls, sub_content: dict, sub_key: str):
        if sub_key in sub_content:
            return sub_content[sub_key]
        else:
            return None

    @classmethod
    def get_arg_overrides(cls, overridekey: str) -> Namespace:
        all_overrides = cls.get_config_value(cls.key_argoverrides)
        args_json = cls.get_inner_value(all_overrides, overridekey)
        args = Namespace(**args_json)
        return args

    @classmethod
    def _init_config_data(cls):
        """Initialize the config data once"""
        try:
            with open(f"{cls.config_path}", "r") as jsonfile:
                cls.config_content = json.load(jsonfile)
        except FileNotFoundError:
            raise ConfigException(f"Config file not found at {cls.config_path}. Hint: You can define the location of the JSON config file by overriding the ConfigUtilBase.config_path not found.")


    @classmethod
    def _read_dict_value(cls, the_dict, the_key):
        if the_key in the_dict:
            return the_dict[the_key]
        else:
            return None