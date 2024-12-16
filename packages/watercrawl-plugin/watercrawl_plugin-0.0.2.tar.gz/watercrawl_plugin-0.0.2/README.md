# Watercrawl Plugin

[![PyPI version](https://badge.fury.io/py/watercrawl-plugin.svg)](https://badge.fury.io/py/watercrawl-plugin)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Description

WaterCrawl plugin is a Python package that provides a base for creating plugins for the WaterCrawl web crawling framework. It offers abstract classes and interfaces to standardize plugin development.

## Installation

You can install the WaterCrawl plugin package using pip:

```bash
pip install watercrawl-plugin
```
Usage
To create a new plugin for Watercrawl, you need to extend the base classes provided by this package. Here's a basic guide on how to create a new plugin:

Import the necessary classes:

```python
from watercrawl_plugin import AbstractPlugin, AbstractPipelinePlugin, AbstractInputValidator
```
Create your plugin class by extending AbstractPlugin:


```python
class MyPlugin(AbstractPlugin):
    @classmethod
    def get_name(cls) -> str:
        return "MyPlugin"

    @classmethod
    def get_description(cls) -> str:
        return "This is my custom plugin for WaterCrawl"

    @classmethod
    def get_version(cls) -> str:
        return "0.1.0"

    @classmethod
    def get_author(cls) -> str:
        return "Your Name"

    @classmethod
    def get_pipeline_class(cls):
        return MyPipelinePlugin

    @classmethod
    def get_input_validator(cls):
        return MyInputValidator
```


Create a pipeline plugin by extending AbstractPipelinePlugin:

```python
class MyPipelinePlugin(AbstractPipelinePlugin):
    def process_item(self):
        # Implement your item processing logic here
        # You can access self.item, self.spider, self.crawler_service, and self.helpers
        pass
```

Create an input validator by extending AbstractInputValidator:

```python
class MyInputValidator(AbstractInputValidator):
    def validate(self):
        # Implement your input validation logic here
        # You can access self.crawler_service, self.helpers, and self.errors
        pass
```

## API Reference
For detailed information about the base classes and their methods, refer to the source code in src/watercrawl_plugin/base.py.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

