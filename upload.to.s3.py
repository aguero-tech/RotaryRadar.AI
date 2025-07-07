import boto3
from datetime import datetime
import os

BUCKET_NAME = 'gurnee-rotary'
EXPORT_DIR = 'exports'

def upload_to_s3():
    today_str = datetime.today().strftime('%Y%m%d')
    file_name = os.path.join(EXPORT_DIR, f'{today_str}.html')
    s3_key = f'{today_str}.html'

    s3 = boto3.client('s3')
    # Upload today's summary file
    s3.upload_file(
        file_name,
        BUCKET_NAME,
        s3_key,
        ExtraArgs={'ContentType': 'text/html'}
    )
    print(f'Uploaded {file_name} to https://{BUCKET_NAME}.s3.amazonaws.com/{s3_key}')

    # Upload index.html
    index_file = os.path.join(EXPORT_DIR, 'index.html')
    s3.upload_file(
        index_file,
        BUCKET_NAME,
        'index.html',
        ExtraArgs={'ContentType': 'text/html'}
    )
    print(f'Uploaded {index_file} to https://{BUCKET_NAME}.s3.amazonaws.com/index.html')

if __name__ == "__main__":
    upload_to_s3()
