import pkgutil
import importlib
import inspect
import elbchecker.checks


def list_load_balancer(client):
    paginator = client.get_paginator('describe_load_balancers')
    pages = paginator.paginate(PaginationConfig={'PageSize': 5})
    for page in pages:
        for elb in page.pop('LoadBalancerDescriptions'):
            yield elb


def list_elb_checks():
    for finder, mod_name, ispkg in pkgutil.iter_modules(elbchecker.checks.__path__):
        check_module = importlib.import_module(f'elbchecker.checks.{mod_name}')
        for name, func in inspect.getmembers(check_module, inspect.isfunction):
            if name.startswith('check_'):
                yield f'{mod_name}.{name}', func


def check_elb(session):
    """
    Perform all elb checks on all elbs for a given region.
    :param session: boto3 session.
    :return: generator that yield the results as a tuple (<name of the check>, <elb name>, <check result>)
    """
    client = session.client('elb')
    for elb in list_load_balancer(client):
        for check_name, check in list_elb_checks():
            name, status = check(session, elb)
            yield (check_name, name, status)


__all__ = ['check_elb']
