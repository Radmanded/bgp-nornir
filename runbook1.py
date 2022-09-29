from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result


nr = InitNornir(config_file="config.yaml") # Initialize Nornir with config.yaml file in same directory as script

results = nr.run(task=send_command, command="show ntp status") # Run show version on all devices in inventory

print_result(results) # Print results of show version
