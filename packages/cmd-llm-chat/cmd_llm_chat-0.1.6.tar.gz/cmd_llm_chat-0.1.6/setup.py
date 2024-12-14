from setuptools import setup, find_packages

setup(
    name='cmd_llm_chat',
    version='0.1.6',
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
