from setuptools import setup , find_packages
import LunarAI

setup(
    name='LunarAI' ,
    version=LunarAI.__version__,
    description='A convenient AI tool',
    long_description=open('README.md',mode='r',encoding='utf-8').read(),
    long_description_content_type = 'text/markdown',
    author='Haozhe Xu',
    author_email='2779630178@qq.com',
    maintainer='Haozhe Xu',
    maintainer_email='2779630178@qq.com',
    license='MIT License',
    packages=find_packages(),
    platforms=['all'],
    url='https://github.com/Haozhe-py/LunarAI',
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        #'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.13',
        'Topic :: Software Development :: Libraries'
    ]
)