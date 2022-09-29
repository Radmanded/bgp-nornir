import requests


def get_api():
    # Get API
    url = "https://www.peeringdb.com/api/netixlan?net_id=3179"  # 3179
    response = requests.get(url)
    data = response.json()["data"]

    # ------------- Process Jinja2 template --------------

    # Import jinja2 module
    from jinja2 import Environment, PackageLoader, select_autoescape
    env = Environment(
      #  loader=PackageLoader("asn"),
        autoescape=select_autoescape()
    )

    # Load template file
    template = env.get_template("config.j2")

    # Render template to stdout
    return template.render(bgp=data)


from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir.core.task import Result, Task
from nornir_napalm.plugins.tasks import napalm_configure

nr = InitNornir(config_file="config.yaml")


def task_1(task: Task, number: int) -> Result:
    n = get_api()
    #   return Result(host=task.host, result=f"{n}")
    return Result(host=task.host, result=f"Configured BGP on {task.host}")


from napalm import get_network_driver
import sys


def deploy_config(task: Task, dry_run: bool = True) -> Result:
    config_rendered = get_api()

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


def main(task=None):
    result = nr.run(task=task_1, number=2)
    print_result(result)


if __name__ == "__main__":
    main()
