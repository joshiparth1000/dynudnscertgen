import sys
from sewer import client, config
from sewer.crypto import AcmeKey, AcmeAccount, KeyDesc
from dynu import DynuDns
import os
import OpenSSL.crypto
from datetime import datetime
import time

def main(args):
    cert_path = '/target/certificate.crt'
    cert_key_path = '/target/certificate.key'
    acct_key_path = '/conf/account.key'

    if os.path.exists(cert_path):
        cert = open(cert_path, 'r')
        cert = cert.read().split('-----END CERTIFICATE-----')[0] + '-----END CERTIFICATE-----'
        cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
        utc_time = datetime.strptime(cert.get_notAfter().decode(), "%Y%m%d%H%M%SZ")
        expiry_time = (utc_time - datetime(1970, 1, 1)).total_seconds()
        cur_time = datetime.now().timestamp()

        if cur_time + 24*60*60 < expiry_time:
            return

    if not os.path.exists(cert_key_path):
        AcmeKey.create("rsa2048").write_pem(cert_key_path)
    if not os.path.exists(acct_key_path):
        account = AcmeAccount.create("rsa2048")
        account.write_pem(acct_key_path)
        is_new_acct = True
    else:
        acct_key = open(acct_key_path, 'rb')
        account = AcmeAccount.from_pem(acct_key.read())
        is_new_acct = False

    cert_key = open(cert_key_path, 'rb')
    cert_key = AcmeKey.from_pem(cert_key.read())
    dns_class = DynuDns(api_key=os.getenv('API_KEY'))

    success = False
    i = 1
    
    while i <=5 and not success:
        try :
            acme_client = client.Client(
                domain_name='*.' + os.getenv('DOMAIN'),
                domain_alt_names=[os.getenv('DOMAIN')],
                provider=dns_class,
                account=account,
                cert_key=cert_key,
                is_new_acct=is_new_acct,
                ACME_DIRECTORY_URL=config.ACME_DIRECTORY_URL_PRODUCTION,
                ACME_AUTH_STATUS_WAIT_PERIOD=30,
                ACME_AUTH_STATUS_MAX_CHECKS=10
            )

            certificate = acme_client.get_certificate()

            with open(cert_path, 'w') as certificate_file:
                certificate_file.write(certificate)
            
            success = True
        except:
            time.sleep(3 ** i)
        finally:
            i += 1



if __name__ == '__main__':
    main(sys.argv[1:])
