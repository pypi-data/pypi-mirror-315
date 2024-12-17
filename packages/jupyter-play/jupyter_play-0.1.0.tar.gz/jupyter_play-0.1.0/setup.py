from setuptools import setup 


from setuptools import find_packages
from setuptools.command.build_py import build_py

import os 
import zipfile
import logging 
import subprocess

import warnings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class my_build_py(build_py): 
    """Custom build step to unzip packaged html files"""
    def run(self):

        cur_dir = os.getcwd()
        src_dir = os.path.join('src', 'jupyter_play')
        html_zip = os.path.join(src_dir, 'html_games.zip')

        logger.debug(f'CUR_DIR: ({os.path.abspath(cur_dir)}): ' + ', '.join(os.listdir(cur_dir)))
        logger.debug('PACKAGE_DIR (src): ' + ', '.join(os.listdir(src_dir)))


        if not os.path.exists(html_zip):

            error_msg = f"Missing '{html_zip}. Attempting to run download script 'download_games.sh' before building package."
            logger.error(error_msg)
            raise Exception(error_msg)

        extract_to = os.path.abspath(os.path.join(src_dir, 'html_games'))        
        os.makedirs(extract_to, exist_ok=True)
        logger.debug(f'EXTRACTING TO: {extract_to}')
            
        with zipfile.ZipFile(html_zip, 'r') as zip_ref: 
            zip_ref.extractall(extract_to)
        
        # Continue with standard build process
        super().run()

setup(
    name='jupyter-play',
    version="0.1.0",
    package_dir={"":"src"},
    packages=find_packages(where="src", exclude=("test*", "testing*", "tests*")),
    cmdclass={'build_py':my_build_py},
    # include_package_data=True,
    package_data={
        'jupyter_play':[
            '*.zip',
            'logging_configs.json',
            'html_games/*.html'
        ]
    }
)