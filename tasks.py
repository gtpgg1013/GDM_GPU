# from celery import Celery
# import shutil
# import os
# import zipfile
# from pathlib import Path


# app = Celery('tasks', broker='pyamqp://guest@localhost//')

# # 요런 task라는 프로세스를 띄워놓고 계속 써먹게 하면 되는?

# @app.task
# def add(x, y):
#     return x + y

# @app.task
# def _inference(rds_id, num_trial):
#     base_nas_path = '/mnt/c/Users/user/OneDrive/바탕 화면/GAN 때문이야/WEB Service/WEB/media'
#     # loaded_model = 'model'Settings
    
#     # 생성된 이미지 저장하는 folder 생성
#     result_dir_path = os.path.join(base_nas_path, 'dataset', 'result_dataset', str(rds_id), str(num_trial) + 'th')
#     image_dir_path = os.path.join(result_dir_path, 'images')
#     zip_dir_path = os.path.join(result_dir_path, 'zip_dir')
#     print(result_dir_path)
#     os.makedirs(result_dir_path, exist_ok=True)
#     os.makedirs(image_dir_path, exist_ok=True)
#     os.makedirs(zip_dir_path, exist_ok=True)

#     # for문 활용 inference 수행
#     '''
#     TBD
#     '''

#     # 생성된 이미지 NAS 저장
#     ## inference image NAS 저장
#     ### sample 복사로 test code에서는 대체
#     sample_image_path = os.path.join(base_nas_path, 'sample.PNG')
#     result_file_path_list = []

#     for i in range(5):
#         result_file_path = os.path.join(image_dir_path, 'sample_{}th_{}.png'.format(num_trial, i))
#         shutil.copy(sample_image_path, result_file_path)
#         result_file_path_list.append(result_file_path)

#     # 그리고 meta정보도 싹다 넘겨야함
#     # ResultDatasetImage
#     # Path / Name만 일단 있으면 됨.
#     # result_file_path_list 에 저장됨.

#     # 생성된 이미지 zip으로 만들어서 NAS 저장
    
#     zip_path = os.path.join(zip_dir_path, '{}_rds.zip'.format(rds_id))
#     if not os.path.exists(zip_path):
#         zip_file = zipfile.ZipFile(zip_path, 'w')
#         for result_file_path in Path(image_dir_path).rglob("*"):
#             zip_file.write(result_file_path, result_file_path.name, compress_type=zipfile.ZIP_DEFLATED)

#         zip_file.close()

#     # list에 생성된 이미지 path 저장
#     # 다시 django에게 통신 보냄 (django쪽에서 YN값 변경)
    
#     return {"rds_id": rds_id}