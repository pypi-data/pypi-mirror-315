from setuptools import setup, find_packages

setup(
    name='phg_vis',  # 包名
    version='0.0.1',  # 版本号
    packages=find_packages(),  # 自动找到包
    include_package_data=True,  # 包含非Python文件
    description='A package for phg modeling language',  # 简短描述
    long_description=open('README.md').read(),  # 详细描述
    long_description_content_type='text/markdown',
    author='romeosoft',
    author_email='18858146@qq.com', 
    url='https://github.com/panguojun/phg',
    classifiers=[ 
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.13',
    install_requires=[],
    package_data={
        'phg': ['phg.pyd'],
    },
)