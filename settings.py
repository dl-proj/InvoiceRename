import os

from utils.folder_file_manager import make_directory_if_not_exists

CUR_DIR = os.path.dirname(os.path.abspath(__file__))

PDF_IMAGES_DIR = make_directory_if_not_exists(os.path.join(CUR_DIR, 'pdf_images'))
CONFIG_FILE = os.path.join(CUR_DIR, 'config.cfg')
