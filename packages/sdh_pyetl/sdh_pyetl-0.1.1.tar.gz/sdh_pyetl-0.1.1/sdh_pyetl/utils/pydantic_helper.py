import importlib
import inspect
import json
import os
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel

from .exceptions import ModelNotFound


def load_config(config_file_path: str, step: Literal["source", "destination"], name: str) -> BaseModel:
    models = load_models_from_module(os.path.join("etl/configs/", step))
    pydantic_model = models.get(name.lower())
    if not pydantic_model:
        raise ModelNotFound(f"'{name}' not found in {list(models.keys())}")

    file_extension = config_file_path.split(".")[-1]
    with open(config_file_path, encoding="utf8") as file:
        if file_extension == "json":
            config_data = json.load(file)
        elif file_extension == "yaml":
            config_data = yaml.safe_load(file)
        else:
            raise ValueError("Unsupported config format, use json or yaml.")

    return pydantic_model(**config_data)


# Function to dynamically load models from Python files in a submodule
def load_models_from_module(module_path: str) -> dict[str, type]:
    model_map = {}

    # Traverse the submodule directory and import each Python file
    module_dir = Path(module_path)

    if not module_dir.is_dir():
        raise ValueError(f"The provided path {module_path} is not a directory")

    # Iterate over all Python files in the directory
    for py_file in module_dir.glob("*.py"):

        # Get the module name from the file path
        module_name = py_file.stem

        # Dynamically import the module
        module = importlib.import_module(f"{module_path.replace('/', '.')}.{module_name}")

        # Iterate over all classes in the module and check if they are Pydantic models
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, BaseModel) and obj is not BaseModel:
                model_map[name.lower()] = obj

    return model_map
