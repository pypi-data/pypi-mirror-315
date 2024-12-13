# setup.py
from setuptools import setup, find_packages

setup(
    name="zerpy",
    version="1.0.0",
    author="MohamedLunar",
    author_email="contact.mohamedlunardev@gmail.com",
    description="🔗 Package Guide On https://github.com/MohamedLunar/zerpy",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MohamedLunar/zerpy",  # URL لمستودع GitHub الخاص بك
    packages=find_packages(),
    install_requires=[
        "python-dotenv",  # مكتبة تحميل المتغيرات البيئية
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
