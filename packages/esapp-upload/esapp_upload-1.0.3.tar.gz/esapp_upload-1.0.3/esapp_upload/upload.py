# -*- coding: utf-8 -*-
import requests
import os
from requests_toolbelt.multipart.encoder import MultipartEncoder

def upload_es_app(package_name, version, file_path, is_production, refresh, remark):
    url = 'http://api.extscreen.com/v1/tvpver/deploy' if is_production else 'http://test-api.extscreen.com/v1/tvpver/deploy'
    
    # 根据环境选择相应的token
    token_env_var = 'ESAPP_PROD_TOKEN' if is_production else 'ESAPP_TEST_TOKEN'
    header = os.getenv(token_env_var)
    if not header:
        raise ValueError(f"Environment variable {token_env_var} is not set.")
    print(header)
    headers = {
        'Content-Type': 'multipart/form-data',
        'deploy-token': header
    }
    
    multipart_data = MultipartEncoder(
        fields={
            'package_name': package_name,
            'package_ver': version,
            'refresh': refresh,
            'remark': remark,
            'files': (os.path.basename(file_path), open(file_path, 'rb'))
        }
    )
    
    headers['Content-Type'] = multipart_data.content_type
    
    response = requests.post(url, headers=headers, data=multipart_data)
    
    if response.status_code == 200:
        print("Upload successful!")
    else:
        print(f"Upload failed with status code {response.status_code}: {response.text}")

# 示例调用
if __name__ == "__main__":
    upload_es_app(
        package_name="es.huan.cece.com",
        version="1.0.2",
        file_path="android.zip",
        is_production=False,
        refresh="0",
        remark="example remark"
    )