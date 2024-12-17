from setuptools import setup, find_packages

setup(
    name='langchain-yt-dlp',
    version='0.0.3',
    description='YouTube loader for LangChain using yt-dlp',
    long_description=open('README.md').read(),
    url="https://github.com/aqib0770/langchain-yt-dlp",
    author='Aqib Ansari',
    author_email='aqibansari72a@gmail.com',
    packages=find_packages(exclude=['tests*']),
    long_description_content_type='text/markdown',
    keywords='langchain yt-dlp youtube-transcript-api loader',
    install_requires=[
        'yt-dlp',
        'langchain',
        'youtube-transcript-api'
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.8',
)