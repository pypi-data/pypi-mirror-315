# Pergola project tools

Helpful tools and utils for applications running inside of [Pergola](https://console.pergola.cloud/) , the beautifully simple internal developer platform

# Installation

```bash
pip install pergola-projecttools
```

# Getting started

## Configuration Management

Pergola offers secure stage specific configurations, which can easily by copied, adjusted and swapped. projecttools provides a simple but powerful approach to leverage those in your python application.
See [Pergola Configuration Management](https://docs.pergola.cloud/docs/reference/configurations) for details on the concept.

The class ```ConfigUtilBase``` provides access to a config-file mapped from Pergola configuration management.

### How ConfigUtilBase provides access to a JSON config file

1) At first, in your application, provide a path for config-files. Create a subdirectory named config and make sure it gets pushed to git (or your VCS provider). This can e.g. be enforced by adding a .gitignore file with the this content there:
```gitignore
*.json
!config.template.json
```
Note: This has the additional benefit of never accidentally commiting any json config files with passwords or other secrets.

2) Put a file called ```config.json``` into the config subdirectory. Add some config values into the file, e.g.
```json
{
  "username": "John",
  "appearance": {
      "theme": "dark",
      "size": 500
  }
}
```

3) Use ```ConfigUtil``` to access your config utils, either quick or more sophisticated

the quick and simple method:
```python
from pergolaprojecttools.config_util import ConfigUtilBase

# Use it right away
ConfigUtilBase.get_config_value("username") # returns 'John'
ConfigUtilBase.get_config_value("appearance") # returns a dict with 'theme' and 'size'
```


or the sophisticated method:

Create a class ```ConfigUtil``` inheriting from ```ConfigUtilBase``` and add get methods for all your config parameters, ensuring a safe usage.
This approach also gives you more control, e.g. to specify the config file path or to navigate deeper into your JSON structure. For our example, this could look like:

```python
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

```python
    the_user_name = ConfigUtil.get_user()
```

Try this locally, it works during development, in IDEs like Visual Studio or toolings like Jupyter


4) To provide configurations in Pergola, got to the Config Management of a Pergola stage. Create a file called my-stage-config.json (named appropriately for your purpose).


5) Map the file in Pergola Manifest:
```yaml
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
  Note, that this has the additional benefit of never accidentally commiting any json config files with passwords or other secrets.

 
And never forget: Do not put passwords or other secrets into your source code, always use a secure Pergola config!

### Define config file location

To define an individual location for the config file, override the class variable ```config_path``` of ```ConfigUtilBase```, e.g.


```python
ConfigUtilBase.config_path = 'configuration/app_central.json'
```

Or, with subclassing and more versatile path logic:

```python
import os
class ConfigUtil(ConfigUtilBase):

    config_path = f"{os.getcwd()}/configuration/app_central.json"

```

or

```python
import pathlib
class ConfigUtil(ConfigUtilBase):
    config_path = f"{pathlib.Path(__file__).parent}/configuration/app_central.json"
```

## Logging for Pergola

projecttools provides preconfigured simplified logging for [Pergola](https://console.pergola.cloud) applications. 

### Activation
It is activated by calling ```log.init_logging()```. Parameters to tailor the behaviour may be used, but it works out of the box with no parameters at all.

Example:
```python
from pergolaprojecttools import log

log.init_logging()
```

This way, you will automatically receive nice logging output to the console during development as well great logging output in Pergola, including pod runtime identifiers.

### Usage

Simply call the log level methods with your log message:
```python
from pergolaprojecttools import log

log.debug('My debug message')
log.info('My info message')
log.warning('My warning message')
log.error('My error message')

# log last exception with details:
log.logLastException('CONTEXT-INFO')

# add memory usage to log string:
from pergolaprojecttools.trace_util import get_mem
log.info('Important info ' + get_mem())
```

### More control

Call ```log.init_logging()``` with parameters:

logger_basename: used for config of python logging and as part of the filenames
log_folder: folder to store log files in (log_to_file needs to be True)
log_level: one of debug, info, warn, error, default: debug
log_to_file: True/False (at least one of [log_to_file,log_to_console] must be True)
log_to_console: True/False (at least one of [log_to_file,log_to_console] must be True)
log_in_pergola: True/False/None - if None is given, logging will try to detect its environment automatically

### Re-configure at runtime

You can always deactivate logging with 
```python
from pergolaprojecttools import log
log.clear_logging()
```

and reactivate it with properties, e.g.
```python
log.init_logging(logger_basename='central', log_folder='./logs/core/', log_to_file=True) 
```






