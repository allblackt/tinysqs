from unittest.mock import patch, Mock, call

from tinysqs.awsv4signer import sign
from tinysqs.awsv4signer import hash_sha256
from tinysqs.awsv4signer import get_signature_key


@patch('tinysqs.awsv4signer.hmac')
@patch('tinysqs.awsv4signer.hashlib')
def test_sign_default_no_hex(hashlib, hmac):
    key = Mock()
    msg = Mock()

    sign(key, msg)

    hmac.new.assert_called_with(key,
                                msg.encode(),
                                hashlib.sha256)
    msg.encode.assert_any_call('utf-8')
    assert not hmac.new().hexdigest.called
    assert hmac.new().digest.called


@patch('tinysqs.awsv4signer.hmac')
@patch('tinysqs.awsv4signer.hashlib')
def test_sign_with_hex(hashlib, hmac):
    key = Mock()
    msg = Mock()

    sign(key, msg, True)

    hmac.new.assert_called_with(key,
                                msg.encode(),
                                hashlib.sha256)
    msg.encode.assert_any_call('utf-8')
    assert not hmac.new().digest.called
    assert hmac.new().hexdigest.called


@patch('tinysqs.awsv4signer.hashlib')
def test_hash_sha256_default_no_hex(hashlib):
    msg = Mock()
    hash_sha256(msg)
    hashlib.sha256.assert_called_with(msg.encode())
    msg.encode.assert_any_call('utf-8')
    assert hashlib.sha256().digest.called
    assert not hashlib.sha256().hexdigest.called


@patch('tinysqs.awsv4signer.hashlib')
def test_hash_sha256_with_hex(hashlib):
    msg = Mock()
    hash_sha256(msg, True)
    hashlib.sha256.assert_called_with(msg.encode())
    msg.encode.assert_any_call('utf-8')
    assert hashlib.sha256().hexdigest.called
    assert not hashlib.sha256().digest.called


@patch('tinysqs.awsv4signer.sign')
def test_get_signature_key(sign):
    # def f
    sign.side_effect = lambda x, y: str(x) + str(y)
    sk = get_signature_key('key', 'date_stamp', 'region_name', 'service_name')

    calls = [call(b'AWS4key', 'date_stamp'),
             call('b\'AWS4key\'date_stamp', 'region_name'),
             call('b\'AWS4key\'date_stampregion_name', 'service_name'),
             call('b\'AWS4key\'date_stampregion_nameservice_name', 'aws4_request')]
    sign.assert_has_calls(calls)
    assert sk is not None

