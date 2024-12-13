import logging
import yaml
import json
import os
import time
from functools import wraps
import torch
import torch.nn as nn
import numpy as np


class LoggerHelper:
    """
    Utility class for managing logging in the application.
    """

    @staticmethod
    def setup_logger(name="primate", log_file="app.log", level=logging.INFO):
        """
        Sets up a logger.

        Parameters
        ----------
        name : str
            Name of the logger.
        log_file : str
            Path to the log file.
        level : int
            Logging level.

        Returns
        -------
        logging.Logger
            Configured logger instance.
        """
        logger = logging.getLogger(name)
        logger.setLevel(level)
        if not logger.handlers:
            # File Handler
            fh = logging.FileHandler(log_file)
            fh.setLevel(level)
            fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

            # Console Handler
            ch = logging.StreamHandler()
            ch.setLevel(level)
            ch.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))

            logger.addHandler(fh)
            logger.addHandler(ch)

        return logger


class ConfigHelper:
    """
    Utility class for handling YAML and JSON configuration files.
    """

    @staticmethod
    def load_config(file_path):
        """
        Loads configuration from a YAML or JSON file.

        Parameters
        ----------
        file_path : str
            Path to the configuration file.

        Returns
        -------
        dict
            Configuration dictionary.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Configuration file not found: {file_path}")

        _, ext = os.path.splitext(file_path)
        with open(file_path, "r") as file:
            if ext == ".yaml" or ext == ".yml":
                return yaml.safe_load(file)
            elif ext == ".json":
                return json.load(file)
            else:
                raise ValueError(f"Unsupported configuration file format: {ext}")

    @staticmethod
    def save_config(config, file_path):
        """
        Saves configuration to a YAML or JSON file.

        Parameters
        ----------
        config : dict
            Configuration dictionary.
        file_path : str
            Path to save the configuration file.
        """
        _, ext = os.path.splitext(file_path)
        with open(file_path, "w") as file:
            if ext == ".yaml" or ext == ".yml":
                yaml.safe_dump(config, file)
            elif ext == ".json":
                json.dump(config, file, indent=4)
            else:
                raise ValueError(f"Unsupported configuration file format: {ext}")


class TimerHelper:
    """
    Utility class for measuring the execution time of functions.
    """

    @staticmethod
    def timeit(func):
        """
        Decorator for timing a function's execution.

        Parameters
        ----------
        func : function
            The function to time.

        Returns
        -------
        function
            Wrapped function with timing logic.
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            print(f"Execution time for {func.__name__}: {elapsed_time:.4f} seconds")
            return result

        return wrapper


class DeviceHelper:
    """
    Utility class for handling PyTorch device operations.
    """

    @staticmethod
    def get_device():
        """
        Gets the best available device for PyTorch.

        Returns
        -------
        torch.device
            PyTorch device (CUDA or CPU).
        """
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")

    @staticmethod
    def move_to_device(data, device):
        """
        Moves data to the specified device.

        Parameters
        ----------
        data : torch.Tensor or dict or list
            Data to move to the device.
        device : torch.device
            Target device.

        Returns
        -------
        torch.Tensor or dict or list
            Data moved to the specified device.
        """
        if isinstance(data, torch.Tensor):
            return data.to(device)
        elif isinstance(data, dict):
            return {k: v.to(device) if isinstance(v, torch.Tensor) else v for k, v in data.items()}
        elif isinstance(data, list):
            return [v.to(device) if isinstance(v, torch.Tensor) else v for v in data]
        else:
            raise TypeError("Data type not supported for device transfer.")


class PerformanceHelper:
    """
    Utility class for profiling PyTorch model performance.
    """

    @staticmethod
    def profile_model(model, input_size):
        """
        Profiles a PyTorch model for parameters and operations.

        Parameters
        ----------
        model : torch.nn.Module
            The PyTorch model to profile.
        input_size : tuple
            Size of the input tensor.

        Returns
        -------
        dict
            Dictionary with profiling details.
        """
        from torchinfo import summary

        if not isinstance(model, nn.Module):
            raise ValueError("Model must be an instance of torch.nn.Module.")

        print("Profiling model...")
        return summary(model, input_size=input_size)


def set_seed(seed):
    """
    Sets the random seed for reproducibility.

    Parameters
    ----------
    seed : int
        The random seed.
    """
    torch.manual_seed(seed)
    np.random.seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
