from setuptools import setup, find_packages

setup(
    name='S-Clustr-DSL',
    version='1.3.7',
    author='Maptnh@S-H4CK13',
    description='A simple DSL for S-Clustr',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.7',
    install_requires=[
        'certifi==2023.7.22',
        'charset-normalizer==3.3.0',
        'colorama==0.4.6',
        'idna==3.4',
        'loguru==0.7.2',
        'pycryptodome==3.19.0',
        'requests==2.31.0',
        'urllib3==2.0.6',
        'win32-setctime==1.1.0',
        'PyQt5==5.15.9'
    ],
    entry_points={
        'console_scripts': [
            'scc-client=clustr.S_Clustr_Client:main',
            'scc-server=clustr.S_Clustr_Server:main',
            'scc-building=clustr.Building:main',
            'scc-debug-device=clustr.DebugDevice:main',
            'scc-game=clustr.game:main',
            'scc-gen=clustr.Generate:main',
            'scc=clustr.scc:main',
            'scc-test=clustr.scctest:main',
            'scc-testpc=clustr.Testpc:main',
        ],
    },
    include_package_data=True,
    package_data={
        'clustr': ['*.py', '*.conf'],
    },
)