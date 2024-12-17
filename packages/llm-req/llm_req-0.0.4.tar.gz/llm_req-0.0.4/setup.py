
from setuptools import setup, find_packages


setup(name='llm-req',
    version='0.0.4',
    description='llm req client',
    url='https://gitee.com/dark.H/llm-cli.git',
    author='auth',
    author_email='xxx@gmail.com',
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    packages=find_packages(),
    install_requires=['requests','aiohttp','loguru','tqdm'],
    entry_points={
        'console_scripts': ['mroy=llm_req.cmd:main']
    },

)
