from setuptools import find_packages, setup

install_requires = [
    "PyQt5>=5.15.10",
    "typing-extensions>=4.12.2",
    "python-dateutil>=2.9.0",
    "numpy",
    "pyperclip",
]

setup(
    name="PyQt-SiliconUI",
    version="0.0.1",
    packages=find_packages(exclude=["examples"]),
    data_files=[("./siui/gui/icons/packages", ["./siui/gui/icons/packages/fluent_ui_icon_filled.icons",
                                               "./siui/gui/icons/packages/fluent_ui_icon_regular.icons",
                                               "./siui/gui/icons/packages/fluent_ui_icon_light.icons"]), ],
    include_package_data=True,
    install_requires=install_requires,
    description="A powerful and artistic UI library based on PyQt5",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ChinaIceF/PyQt-SiliconUI",
    author="ChinaIceF",
    author_email="ChinaIceF@outlook.com",
    license="GPL-3.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        # "License :: OSI Approved :: GPL-3.0 License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    entry_points={
        "console_scripts": [
            ""
        ],
    },
)
