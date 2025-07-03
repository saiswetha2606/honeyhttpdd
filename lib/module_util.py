import os
import importlib

def import_module(directory, module_name):
    """
    Imports and returns the class named module_name from a Python file named module_name.py
    located inside the given directory.
    Returns None if the module or class does not exist.
    """
    if module_exists(directory, module_name):
        try:
            # Convert directory path to Python package style (dots)
            package_path = directory.replace("/", ".").replace("\\", ".")
            
            # Full module path, e.g. honeyhttpdd.loggers.FileLogger
            full_module_path = f"honeyhttpdd.{package_path}.{module_name}"
            
            # Import the module dynamically
            temp_module = importlib.import_module(full_module_path)
            
            # Retrieve the class from the module
            module_class = getattr(temp_module, module_name)
            
            return module_class
        
        except (ModuleNotFoundError, AttributeError) as e:
            print(f"Error importing {module_name} from {full_module_path}: {e}")
            return None
    else:
        return None


def module_exists(directory, module_name):
    """
    Checks if the module file exists in the given directory.
    """
    # Adjust path to work cross-platform
    module_path = os.path.join(".", directory, f"{module_name}.py")
    return os.path.isfile(module_path)
