from setuptools import setup, find_packages 

setup(
    name= "addonev2", # 包名，发布后可用 pip 安装
    version= "1.0.0", # 版本号
    description="A simple package to add 1 to a given number",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your_email@example.com",
    url="https://github.com/yourusername/addone", # 你的项目地址
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entrypoints={
        "console_scripts": [
            "addonev2=addonev2.main:add_one", # 将 `addone` 命令行映射到 `add_one` 函数
        ],
    },
)
