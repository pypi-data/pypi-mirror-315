from primate.utils.helpers import LoggerHelper, ConfigHelper, TimerHelper, DeviceHelper, PerformanceHelper, set_seed
import torch
import torch.nn as nn
import time

# Test LoggerHelper
print("Testing LoggerHelper...")
logger = LoggerHelper.setup_logger(name="test_logger", log_file="test.log")
logger.info("This is an info log.")
logger.error("This is an error log.")

# Test ConfigHelper
print("\nTesting ConfigHelper...")
config = {"model": "bert-base-uncased", "batch_size": 16, "learning_rate": 0.001}
ConfigHelper.save_config(config, "test_config.yaml")
loaded_config = ConfigHelper.load_config("test_config.yaml")
print("Loaded Config:", loaded_config)

# Test TimerHelper
@TimerHelper.timeit
def slow_function():
    time.sleep(2)
    return "Finished!"

print("\nTesting TimerHelper...")
print(slow_function())

# Test DeviceHelper
print("\nTesting DeviceHelper...")
device = DeviceHelper.get_device()
print("Using Device:", device)

data = torch.randn(3, 3)
moved_data = DeviceHelper.move_to_device(data, device)
print("Data on Device:", moved_data.device)

# Test PerformanceHelper
print("\nTesting PerformanceHelper...")
class SimpleModel(nn.Module):
    def __init__(self):
        super(SimpleModel, self).__init__()
        self.linear = nn.Linear(10, 5)

    def forward(self, x):
        return self.linear(x)

model = SimpleModel()
profile = PerformanceHelper.profile_model(model, input_size=(1, 10))
print(profile)

# Test set_seed
print("\nTesting set_seed...")
set_seed(42)
print("Random Number:", torch.rand(1).item())
