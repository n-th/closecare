Privacy for documents visualization

account(id, employee_id, account_id, storage_platform)

Map between documents and a storage platform

## Example

import boto
import boto.s3.connection
access_key = 'put your access key here!'
secret_key = 'put your secret key here!'

conn = boto.connect_s3(
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key,
        host = 'objects.dreamhost.com',
        calling_format = boto.s3.connection.OrdinaryCallingFormat(),
        )

def set_acl(account_id, document_id, permission):
    plans_key = bucket.get_key('secret_plans.txt')
    plans_key.set_canned_acl('private')

def get_url(document_id):
    url = key.generate_url(0, query_auth=False, force_http=True)

    return url


## Document lifecycle
RH companies need to keep documents for a long timebox.

Storage plataforms usually provide different costs for different rates document retrievals.

"Storage class for automatically optimizing data with changing or unknown access patterns. S3 Intelligent-Tiering is an Amazon S3 storage class designed to optimize storage costs by automatically moving data to the most cost-effective access tier, without performance impact or operational overhead.Storage class for automatically optimizing data with changing or unknown access patterns. S3 Intelligent-Tiering is an Amazon S3 storage class designed to optimize storage costs by automatically moving data to the most cost-effective access tier, without performance impact or operational overhead.


## Considerations
Quantidade de updates de doc