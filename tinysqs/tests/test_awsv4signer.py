from unittest.mock import patch
import pytest
from tinysqs.awsv4signer import AWSV4Signer


def test_default_attributes():
    assert AWSV4Signer.method == 'POST'
    assert AWSV4Signer.content_type == 'application/x-www-form-urlencoded'
    assert AWSV4Signer.algorithm == 'AWS4-HMAC-SHA256'
    assert AWSV4Signer.host_pattern == '{service}.{region}.amazonaws.com'
    assert AWSV4Signer.endpoint_pattern == 'https://{host}'


@pytest.mark.parametrize('access_key, secret_key',
                         [('0ayoI8kMpz', 'bl5QUuNV4m'),
                          ('pTn26zk6SI', 'qACmZOABzd'),
                          ('EHDeX1s3Wx', 'KFqjRMv9DP'),
                          ('W6RXOuwq0q', '932pxh8Eag'),
                          ('88PnO4vHuy', '0HRK6j4ZsT')])
def test_init(access_key, secret_key):
    obj = AWSV4Signer(access_key, secret_key)
    assert obj.access_key == access_key
    assert obj.secret_key == secret_key


def test_sign_request_path_error():
    with pytest.raises_regexp(ValueError,
                              'The `path` parameter must always start with / \(forwardslash\)\.'):
        AWSV4Signer('access_key', 'secret_key').sign_request(None,
                                                             None,
                                                             None,
                                                             'bad_path')


@patch('tinysqs.awsv4signer.datetime')
@patch.object(AWSV4Signer, 'endpoint_pattern')
@patch.object(AWSV4Signer, 'host_pattern')
@pytest.mark.xfail
def test_sign_request(host_pattern, endpoint_pattern, datetime):
    signer = AWSV4Signer('access_key', 'secret_key')
    signer.sign_request('service', 'region', 'params')
    print(host_pattern, endpoint_pattern)
