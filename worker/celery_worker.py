from time import sleep

from .celery_app import celery_app

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

import shutil
import os
import zipfile
from pathlib import Path
import requests
import time
from glob import glob
from .algorithm import inference_diffusion_projected_gan

@celery_app.task(acks_late=True)
def _inference(item_dict):
    rds_id = item_dict['rds_id']
    target_data_num = item_dict['target_data_num']
    target_class_list = item_dict['target_class_list']
    model_weight_path = item_dict['model_weight_path']
    algorithm = item_dict['algorithm']
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
    if algorithm == 'Diffusion_Projected_GAN':
        for cls in target_class_list:
            inference_diffusion_projected_gan(image_dir_path, target_data_num, cls, model_weight_path)

    # 생성된 이미지 zip으로 만들어서 NAS 저장

    result_file_path_list = [ele for ele in glob(os.path.join(image_dir_path, '**'), recursive=True)]

    zip_path = os.path.join(zip_dir_path, '{}_rds'.format(rds_id))

    shutil.make_archive(zip_path, 'zip', image_dir_path)
    zip_path += '.zip'
    # list에 생성된 이미지 path 저장
    # 다시 django에게 통신 보냄 (django쪽에서 YN값 변경)

    # Retrieve the CSRF token first
    URL = 'http://127.0.0.1:8000/gan_dm/finish_rds/{}/'.format(rds_id)

    # finish_rds로 다시 통신 ㄱ
    data = {'result_file_path_list' : result_file_path_list, 'zip_path' : zip_path}
    res = requests.post(url=URL, data=data)
    logger.info(str(res))
    # 여기서 통신할 때, 결과들도 다 날려줘야 함

    return {"rds_id": rds_id}