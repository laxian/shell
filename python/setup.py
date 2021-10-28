from setuptools import find_packages, setup

setup(
    name="pull_log",
    version='0.0.9',
    description="The tool for pull log from segway.",
    long_description="""long_description""",

    license='MIT',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    url='hps://github.com/laxian/shell',
    keywords='segway log',
    project_urls={
        "Documentation": "hps://github.com/laxian/shell",
        "Source": "hps://github.com/laxian/shell",
        "Changelog": "hps://github.com/laxian/shell",
    },

    author='zhouweixian',
    author_email='laxian2010@qq.com',

    # package_dir={"": "src"},
    packages=find_packages(exclude=["contrib", "docs", "tests*", "tasks"], ),
    package_data={
        "src.log": ["config.json"],
    },
    install_requires=[
        'certifi==2020.11.8',
        'chardet==3.0.4',
        'idna==2.10',
        'requests==2.25.0',
        'urllib3==1.26.2',
    ],
    entry_points={
        "console_scripts": [
			"segway_box=src.log.cli:segway_box",
			"segway_clear_tasks=src.log.cli:segway_clear_tasks",
			"segway_shield=src.log.cli:segway_shield",
			"segway_broken=src.log.cli:segway_broken",
			"segway_share=src.log.cli:segway_share",
			"segway_arrive=src.log.cli:segway_arrive",
			"segway_available=src.log.cli:segway_available",
			"segway_restore=src.log.cli:segway_restore",
			"segway_status2=src.log.cli:segway_status2",
			"segway_status=src.log.cli:segway_status",
			"segway_upload=src.log.cli:segway_upload",
			"segway_showconfig=src.log.cli:segway_showconfig",
			"segway_query2=src.log.cli:segway_query2",
			"segway_query=src.log.cli:segway_query",
			"segway_pull_sys=src.log.cli:segway_pull_sys",
			"segway_pull_s2=src.log.cli:segway_pull_s2",
			"segway_pull_ex=src.log.cli:segway_pull_ex",
			"segway_pull=src.log.cli:segway_pull",
			"segway_login=src.log.cli:segway_login",
			"segway_nav=src.log.cli:segway_nav",
			"segway_fetch=src.log.cli:segway_fetch",
			"segway_download=src.log.cli:segway_download",
			"segway_config=src.log.cli:segway_config",
			"segway_auto=src.log.cli:segway_auto",
			"segway_adb=src.log.cli:segway_adb",
            "segway=src.log.cli:segway",
        ],
    },

    zip_safe=False,
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',
)
