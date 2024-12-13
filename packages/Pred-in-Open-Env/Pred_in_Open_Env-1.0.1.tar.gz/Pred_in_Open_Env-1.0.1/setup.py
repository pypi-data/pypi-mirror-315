import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Pred_in_Open_Env",
    version="1.0.1",
    author="hzy",
    author_email="bbts123@sjtu.edu.cn",
    description="A model to predict pedestrian flow in open environment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["run", "wrap"],  # 直接指定模块名（不需要包目录）
    package_dir={"": "src"},  # 设置源代码目录为 src
    install_requires=[
        'numpy',  # 例如指定包名
        'pandas',
        'scikit-learn',
        'torch==2.2.2',
        'matplotlib',# 也可以指定版本
    ],
    python_requires=">=3.8",
    include_package_data=True,  # 确保额外文件被包含
    package_data={
        '': ['data/*', 'pyarmor_runtime_000000/*'],  # 包括 data 和 pyarmor 运行时文件
    },
)