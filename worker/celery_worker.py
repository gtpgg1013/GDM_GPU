from time import sleep

from .celery_app import celery_app

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

import shutil
import os
import zipfile
from pathlib import Path
import requests

@celery_app.task(acks_late=True)
def _inference(rds_id):
    
    base_nas_path = '/mnt/c/Users/user/OneDrive/바탕 화면/GAN 때문이야/WEB Service/WEB/media'
    # loaded_model = 'model'Settings
    
    # 생성된 이미지 저장하는 folder 생성
    result_dir_path = os.path.join(base_nas_path, 'dataset', 'result_dataset', str(rds_id))
    image_dir_path = os.path.join(result_dir_path, 'images')
    zip_dir_path = os.path.join(result_dir_path, 'zip_dir')
    print(result_dir_path)
    os.makedirs(result_dir_path, exist_ok=True)
    os.makedirs(image_dir_path, exist_ok=True)
    os.makedirs(zip_dir_path, exist_ok=True)

    # for문 활용 inference 수행
    '''
    TBD
    '''

    # 생성된 이미지 NAS 저장
    ## inference image NAS 저장
    ### sample 복사로 test code에서는 대체
    sample_image_path = os.path.join(base_nas_path, 'sample.PNG')
    result_file_path_list = []

    for i in range(5):
        result_file_path = os.path.join(image_dir_path, 'sample_{}.png'.format(i))
        shutil.copy(sample_image_path, result_file_path)
        result_file_path_list.append(result_file_path)

    # 그리고 meta정보도 싹다 넘겨야함
    # ResultDatasetImage
    # Path / Name만 일단 있으면 됨.
    # result_file_path_list 에 저장됨.

    # 생성된 이미지 zip으로 만들어서 NAS 저장
    
    zip_path = os.path.join(zip_dir_path, '{}_rds.zip'.format(rds_id))
    if not os.path.exists(zip_path):
        zip_file = zipfile.ZipFile(zip_path, 'w')
        for result_file_path in Path(image_dir_path).rglob("*"):
            zip_file.write(result_file_path, result_file_path.name, compress_type=zipfile.ZIP_DEFLATED)

        zip_file.close()

    # list에 생성된 이미지 path 저장
    # 다시 django에게 통신 보냄 (django쪽에서 YN값 변경)
    
    print('sdfdsdffsd')

    # Retrieve the CSRF token first
    URL = 'http://127.0.0.1:8000/gan_dm/finish_rds/{}/'.format(rds_id)

    # finish_rds로 다시 통신 ㄱ
    data = {'result_file_path_list' : result_file_path_list, 'zip_path':zip_path}
    res = requests.post(url=URL, data=data)
    logger.info(str(res))
    # 여기서 통신할 때, 결과들도 다 날려줘야 함 (image_path?)

    return {"rds_id": '32324323'}