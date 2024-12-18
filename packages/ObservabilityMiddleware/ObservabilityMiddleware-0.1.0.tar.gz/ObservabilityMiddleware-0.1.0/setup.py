from setuptools import setup, find_packages

setup(
    name='ObservabilityMiddleware',  # 包名
    version='0.1.0',  # 版本号
    author='rhinuxx',  # 作者
    author_email='rhinux.x@gmail.com',  # 作者邮箱
    description='A middleware for observability in FastAPI applications',  # 简短描述
    long_description=open('README.md').read(),  # 长描述，通常是 README 文件的内容
    long_description_content_type='text/markdown',
    url='https://github.com/rhinuxx/ObservabilityMiddleware',  # 项目主页
    packages=find_packages(),  # 自动查找包
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # 许可证
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Python 版本要求
    install_requires=[
        'fastapi',  # 依赖项
        'python-json-logger',
        # 添加其他依赖项
    ],
)