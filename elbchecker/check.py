checks = {}


def check_elb_cross_zone(client, elb):
    """
    Check if the elb has the cross az option active.
    :param client: boto3 client.
    :param elb: elb information as return by describe elb call.
    :return: typle (name, result) name is the elb name being checked, and result is True/False
        i.e success/failed the check
    """
    name = elb['LoadBalancerName']
    enabled = get_elb_cross_zone_attr(client, name)
    status = "OK" if enabled else "NOK"
    return name, status


checks['cross_zone'] = check_elb_cross_zone


def check_elb_azs(client, elb):
    """
    Check that the elb has at least 2 availability zone setup.
    :param client: boto3 client.
    :param elb: elb information as return by describe elb call.
    :return: typle (name, result) name is the elb name being checked, and result is True/False
        i.e success/failed the check
    """
    zones = elb['AvailabilityZones']
    name = elb['LoadBalancerName']
    status = "OK" if len(zones) > 1 else "NOK"
    return name, status


checks['azs'] = check_elb_azs


def list_load_balancer(client):
    paginator = client.get_paginator('describe_load_balancers')
    pages = paginator.paginate(PaginationConfig={'PageSize': 5})
    for page in pages:
        for elb in page.pop('LoadBalancerDescriptions'):
            yield elb


def get_elb_cross_zone_attr(client, elb_name):
    attr = client.describe_load_balancer_attributes(LoadBalancerName=elb_name)
    attr = attr.pop('LoadBalancerAttributes').pop('CrossZoneLoadBalancing').pop('Enabled')
    return attr


def check_elb(client):
    """
    Perform all elb checks on all elbs for a given region.
    :param client: boto3 elb client.
    :return: generator that yield the results as a tuple (<name of the check>, <elb name>, <check result>)
    """
    for elb in list_load_balancer(client):
        for check_name, check in checks.items():
            name, status = check(client, elb)
            yield (check_name, name, status)


__all__ = ['check_elb']
