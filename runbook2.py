from nornir import InitNornir
from nornir_scrapli.task import send_config
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

def send_config_test(task):
    task.run(task=send_config, config=f"ntp server 55.66.11.33")

results = nr.run(task=random_config)
print_result(results)
