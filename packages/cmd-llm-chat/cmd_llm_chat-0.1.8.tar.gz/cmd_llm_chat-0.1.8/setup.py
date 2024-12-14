from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cmd_llm_chat',
    version='0.1.8',
    author='siy',
    description='基于LLM的命令行工具助手',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'chat=cmd_llm_chat.chat:main',
        ],
    },
    install_requires=[
        'colorama==0.4.6',
        'matplotlib==3.7.1',
        'openai~=1.55.3',
        'prompt_toolkit~=3.0.38',
        'rich==13.9.4',
        'qianfan==0.4.12.1',
        'pyyaml~=6.0',
        'numpy~=1.24.3',
        'pillow~=9.4.0',
    ],
)
