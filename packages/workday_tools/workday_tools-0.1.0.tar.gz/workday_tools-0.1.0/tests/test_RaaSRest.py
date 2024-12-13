import json
import os.path
import logging
import responses
import pytest
from workday_tools_nosrednakram.RaaSRest import RaaSRest


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


def test_RaaSRest_Logging(caplog):
    R = RaaSRest()
    response = R.report(report='RaaSTest')
    assert response is not None
    assert response.status_code == 503
    assert "Connection error connecting to https://PROD_URL/ccx/service/customreport2/TENANT" in caplog.text


def test_RaaSRest_disable_Logging(caplog):
    R = RaaSRest()
    logging.getLogger('workday_tools_nosrednakram.RaaSRest').propagate = False
    R.report(report='RaaSTest')
    assert not "Connection error connecting to https://PROD_URL/ccx/service/customreport2/TENANT" in caplog.text
    logging.getLogger('workday_tools_nosrednakram.RaaSRest').propagate = True


def test_RaaSRest_Report_Not_Found(caplog):
    assert os.path.isfile("secret.yaml") is True
    R = RaaSRest(config_file="secret.yaml")
    response = R.report(report='RaaSTest')
    assert response is not None
    assert response.status_code == 500
    assert "Report not found" in caplog.text


def test_RaaSRest_Run_Report(caplog):
    assert os.path.isfile("secret.yaml") is True
    R = RaaSRest(config_file="secret.yaml")
    response = R.report(report='CR_IHD004_Academic_Period')
    assert response is not None
    assert response.status_code == 200


def test_RaaSRest_Response_Returned(mocked_responses):
    mocked_responses.get(
        "https://PROD_URL/ccx/service/customreport2/TENANT/ACCOUNT/RaaSTest?format=json",
        json={'Report_Entry': [1, 2, 3]},
        status=200,
        content_type="application/json",
    )
    R = RaaSRest()
    response = R.report(report='RaaSTest')
    assert json.loads(response.text) == {'Report_Entry': [1, 2, 3]}
    assert response.status_code == 200
