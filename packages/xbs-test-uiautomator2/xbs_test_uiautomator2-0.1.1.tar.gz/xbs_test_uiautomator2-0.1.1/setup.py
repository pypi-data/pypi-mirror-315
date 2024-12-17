from setuptools import setup, find_packages

setup(
    name='xbs_test_uiautomator2',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'uiautomator2==2.16.25',
    ],
    include_package_data=True,
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ll6566/xbsUiautomator2',
    author='65',
    author_email='18974710587@163.com',
    description='rewrite uiautomator2',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.0.0',
)