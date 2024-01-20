import os
from pathlib import Path


def get_file_names_by_time(directory: str):
    if not os.path.exists('static/images'):
        os.mkdir('static/images')
    return [str(os.path.basename(file_path)) for file_path in sorted(Path(directory).iterdir(), key=os.path.getmtime, reverse=True)]
    
def save_image_file(img_data: bytes) -> str:
    image_file_names = get_file_names_by_time('static/images')
    number_suffix = 1
    
    if len(image_file_names) > 0:
        number_suffix = int(image_file_names[-1].split('_')[-1].split('.')[0]) + 1
    saved_path = f'static/images/image_{number_suffix}.png'
    with open(saved_path, 'wb') as f:
        f.write(img_data)
        
    return saved_path