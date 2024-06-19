from setuptools import setup

setup(
    name="punkweb_insight",
    version="0.0.5",
    author="Punkweb",
    author_email="punkwebnet@gmail.com",
    packages=["punkweb_insight"],
    url="https://github.com/Punkweb/punkweb-insight",
    license="BSD-3-Clause",
    description="Django application that provides visitor and page view tracking and an analytics dashboard for your Django website.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    zip_safe=False,
    include_package_data=True,
    package_data={"": ["README.md"]},
    install_requires=[
        "django>=4.0",
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
)
