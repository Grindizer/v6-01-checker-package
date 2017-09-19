from elbchecker.check import check_elb


def test_elb_check_crosszone(monkeypatch):
    monkeypatch.setattr('elbchecker.check.list_load_balancer', lambda x: [])
    assert list(check_elb(None)) == []
