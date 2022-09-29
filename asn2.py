from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir.core.task import Result, Task
from nornir_napalm.plugins.tasks import napalm_configure
from nornir_jinja2.plugins.tasks import template_file
from napalm import get_network_driver
import sys
import requests

nr = InitNornir(config_file="config.yaml")

def get_api():
    # Get API
    url = "https://www.peeringdb.com/api/netixlan?net_id=3179"  # 3179
    response = requests.get(url)
    return response.json()["data"]


def deploy_config(task: Task, dry_run: bool = True) -> Result:
    data = get_api()

    result_jinja2 = task.run(task=template_file, path="templates", template="config.j2", bgp=data)

    napalm_result = task.run(
        task=napalm_configure,
        dry_run=dry_run,
        configuration=config_rendered,
    )

    return Result(
        host=task.host,
        result=f"{napalm_result.result}",
    )


# show diff
result = nr.run(task=deploy_config, dry_run=True)
print_result(result)

print("Continue: Y/n")
if "n" in input().lower():
    sys.exit(0)

# push change
result = nr.run(task=deploy_config, dry_run=False)
print_result(result)
