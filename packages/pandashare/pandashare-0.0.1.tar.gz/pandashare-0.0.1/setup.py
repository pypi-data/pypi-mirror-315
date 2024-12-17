from setuptools import setup, find_packages

setup(
    name='pandashare',                          # 包名
    version='0.0.1',                             # 版本号
    packages=find_packages(),                   # 自动查找包
    install_requires=[],                        # 依赖（如果有的话）
    long_description=open('README.md').read(),  # 长描述
    long_description_content_type='text/markdown',  # 内容类型
    author='quantdrchow',                         # 作者信息
    author_email='quantdrchow@gmail.com',       # 作者邮箱
    description='Sharing data focused on financial AI',    # 简短描述
    license='MIT',                              # 许可协议
    url='https://github.com/yourusername/simple_pkg',  # 项目链接
    classifiers=[                               # 分类
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
