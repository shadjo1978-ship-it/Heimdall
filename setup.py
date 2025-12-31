"""
Setup script for Heimdall AI Personal Assistant
Configured for Windows platform builds
"""
from setuptools import setup, find_packages
import sys

# Windows-specific requirements
install_requires = [
    'pywin32>=305',  # Windows-specific APIs
]

# Optional dependencies for full functionality
extras_require = {
    'voice': [
        'pyttsx3>=2.90',  # Text-to-speech for Windows
        'SpeechRecognition>=3.10',  # Speech recognition
        'pyaudio>=0.2.13',  # Audio I/O
    ],
    'ai': [
        'openai>=1.0.0',  # AI capabilities
        'anthropic>=0.7.0',  # Alternative AI provider
    ],
    'firewall': [
        'scapy>=2.5.0',  # Packet manipulation
    ],
}

# Include all extra dependencies
extras_require['all'] = [
    dep for deps in extras_require.values() for dep in deps
]

setup(
    name='heimdall',
    version='0.1.0',
    description='AI personal assistant with real-time thinking and voice that also serves as a firewall',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Heimdall Team',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=install_requires,
    extras_require=extras_require,
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'heimdall=heimdall.main:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: Microsoft :: Windows :: Windows 11',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
