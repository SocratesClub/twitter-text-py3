from setuptools import setup, find_packages
 
setup(
    name='twitter-text-py3',
    version='1.0.1',
    description='A library for auto-converting URLs, mentions, hashtags, lists, etc. in Twitter text. Also does tweet validation and search term highlighting.',
    author='Daniel Ryan and Cheng-Jun Wang',
    author_email='wangchj04@126.com',
    url='https://github.com/computational-class/twitter-text-py3',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    include_package_data=True,
    install_requires=['setuptools'],
    license = "BSD"
)