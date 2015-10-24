import hmac
import hashlib
import datetime


def sign(key, msg, hex=False):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).hexdigest() \
        if hex is True else \
        hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()


def hash_sha256(msg, hex=False):
    return hashlib.sha256(msg.encode('utf-8')).hexdigest() \
        if hex is True else \
        hashlib.sha256(msg.encode('utf-8')).digest()


def get_signature_key(key, date_stamp, region_name, service_name):
    kDate = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    kRegion = sign(kDate, region_name)
    kService = sign(kRegion, service_name)
    kSigning = sign(kService, 'aws4_request')
    return kSigning


class AWSV4Signer(object):
    """
    Signs POST requests with the SigV4 standard.
    See other examples at http://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html#signature-v4-examples-python
    """

    method = 'POST'
    content_type = 'application/x-www-form-urlencoded'
    algorithm = 'AWS4-HMAC-SHA256'

    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key

    def sign_request(self, service, region, params, path='/'):
        if not path.startswith('/'):
            raise ValueError("The `path` parameter must always start with / (forwardslash).")

        host = '{service}.{region}.amazonaws.com'.format(region=region, service=service)
        endpoint = 'https://{host}'.format(host=host)

        t = datetime.datetime.utcnow()
        amz_date = t.strftime('%Y%m%dT%H%M%SZ')
        date_stamp = t.strftime('%Y%m%d')  # Date w/o time, used in credential scope

        request_parameters = '&'.join(['='.join([k, v]) for k, v in params.items()])
        payload_hash = hash_sha256(request_parameters, hex=True)

        canonical_uri = path
        canonical_querystring = ''

        canonical_headers = ('content-type:{content_type}\n'
                             'host:{host}\n'
                             'x-amz-date:{amz_date}\n'
                             ).format(content_type=self.content_type,
                                      host=host,
                                      amz_date=amz_date)
        signed_headers = 'content-type;host;x-amz-date'

        canonical_request = '\n'.join([self.method,
                                       canonical_uri,
                                       canonical_querystring,
                                       canonical_headers,
                                       signed_headers,
                                       payload_hash])

        credential_scope = ('{date_stamp}/{region}/{service}/aws4_request'
                            ).format(date_stamp=date_stamp,
                                     region=region,
                                     service=service)

        string_to_sign = '\n'.join([self.algorithm,
                                    amz_date,
                                    credential_scope,
                                    hash_sha256(canonical_request, hex=True)])

        authorization_header = ('{algorithm} Credential={access_key}/{credential_scope}, '
                                'SignedHeaders={signed_headers}, Signature={signature}'
                                ).format(algorithm=self.algorithm,
                                         access_key=self.access_key,
                                         credential_scope=credential_scope,
                                         signed_headers=signed_headers,
                                         signature=sign(get_signature_key(self.secret_key,
                                                                          date_stamp,
                                                                          region,
                                                                          service),
                                                        string_to_sign,
                                                        hex=True))

        headers = {'content-type': self.content_type,
                   'x-amz-date': amz_date,
                   'Authorization': authorization_header}

        return {'url': endpoint + path,
                'headers': headers,
                'data': request_parameters}
