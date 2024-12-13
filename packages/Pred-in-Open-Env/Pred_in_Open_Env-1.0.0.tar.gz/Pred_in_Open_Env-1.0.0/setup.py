import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Pred_in_Open_Env",
    version="1.0.0",
    author="hzy",
    author_email="bbts123@sjtu.edu.cn",
    description="A model to predict pedestrian flow in open environment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
        'numpy',  # 例如指定包名
        'pandas',
        'scikit-learn',
        'torch==2.2.2',
        'matplotlib',# 也可以指定版本
    ],
    python_requires=">=3.8",
)