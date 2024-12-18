# setup.py

from setuptools import setup, find_packages

setup(
    name='indonesian-ai-assistant',
    version='1.0',
    author='Althaf Sachio Zaidan',
    description='A virtual assistant that recognizes speech and responds in Indonesian.',
    packages=find_packages(),
    install_requires=[
        'SpeechRecognition',
        'pyttsx3',
        'PyAudio',  # Include if necessary
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)