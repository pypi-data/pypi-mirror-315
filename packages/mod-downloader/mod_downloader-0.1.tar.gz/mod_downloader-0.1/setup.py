from setuptools import setup, find_packages

setup(
    name='mod_downloader',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'Pillow',
        'customtkinter',
    ],
    entry_points={
        'console_scripts': [
            'mod_downloader=mod_downloader.ui:create_ui',
        ],
    },
)