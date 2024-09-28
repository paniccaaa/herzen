from setuptools import setup, find_packages

setup(
    name='getweatherdatalr3prog',  
    version='0.1.1',  
    author='paniccaaa',
    author_email='semaadamenko1@gmail.com',
    description='A simple package for fetching weather data using OpenWeatherMap API',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/paniccaaa/herzen/tree/course3',  # Ссылка на репозиторий проекта
    packages=find_packages(),
    install_requires=[
        'requests',
        'pytest'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
