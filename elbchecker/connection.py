from boto3 import session as boto3_session


def get_session(account, region):
    return boto3_session.Session(region_name=region, **account)


def get_client(service_name, session):
    return session.client(service_name)


__all__ = ['get_client', 'get_session']
