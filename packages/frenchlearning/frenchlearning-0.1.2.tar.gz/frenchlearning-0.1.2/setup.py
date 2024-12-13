from setuptools import setup, find_packages

setup(
    name="frenchlearning",
    version="0.1.2",
    author="Tianyi Xia, Litao Zheng",
    author_email="kevinhsia6@gmail.com, zhenglitao0305@gmail.com",
    description="A Python package for learning French, including memorization and quizzing modules.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tianyi-xia1/project-step-3.git",
    packages=[
    "frenchlearning",
    "frenchlearning.memorization",
    "frenchlearning.quiz",
   ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Education",
    ],
    python_requires=">=3.9",
    install_requires=[],
    include_package_data=True,
)
