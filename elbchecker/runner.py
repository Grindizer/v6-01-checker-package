from pkg_resources import iter_entry_points


def list_load_balancer(client):
    paginator = client.get_paginator('describe_load_balancers')
    pages = paginator.paginate(PaginationConfig={'PageSize': 5})
    for page in pages:
        for elb in page.pop('LoadBalancerDescriptions'):
            yield elb


def list_elb_checks():
    for entry in iter_entry_points('elbchecker.checks'):
        try:
            check = entry.resolve()
        except Exception as error:
            # error loading check entrypoint !
            # for now just ignore the entrypoint.
            pass
        else:
            yield entry.name, check


def check_elb(client):
    """
    Perform all elb checks on all elbs for a given region.
    :param client: boto3 elb client.
    :return: generator that yield the results as a tuple (<name of the check>, <elb name>, <check result>)
    """
    for elb in list_load_balancer(client):
        for check_name, check in list_elb_checks():
            name, status = check(client, elb)
            yield (check_name, name, status)


__all__ = ['check_elb']
