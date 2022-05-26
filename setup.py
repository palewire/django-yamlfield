import os
from distutils.core import Command

from setuptools import find_packages, setup


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


def version_scheme(version):
    """
    Version scheme hack for setuptools_scm.

    Appears to be necessary to due to the bug documented here: https://github.com/pypa/setuptools_scm/issues/342

    If that issue is resolved, this method can be removed.
    """
    import time

    from setuptools_scm.version import guess_next_version

    if version.exact:
        return version.format_with("{tag}")
    else:
        _super_value = version.format_next_version(guess_next_version)
        now = int(time.time())
        return _super_value + str(now)


def local_version(version):
    """
    Local version scheme hack for setuptools_scm.

    Appears to be necessary to due to the bug documented here: https://github.com/pypa/setuptools_scm/issues/342

    If that issue is resolved, this method can be removed.
    """
    return ""


class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from django.conf import settings

        settings.configure(
            DATABASES={
                "default": {"NAME": ":memory:", "ENGINE": "django.db.backends.sqlite3"}
            },
            MIDDLEWARE_CLASSES=(),
            INSTALLED_APPS=("yamlfield",),
        )
        import django
        from django.core.management import call_command

        django.setup()
        call_command("test", "yamlfield")


setup(
    name="django-yamlfield",
    author="Ben Welsh",
    author_email="b@palewi.re",
    url="https://palewi.re/docs/django-yamlfield/",
    description="A Django database field for storing YAML data",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
    install_requires=("PyYAML>=3.10"),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Framework :: Django",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 4.0",
        "License :: OSI Approved :: MIT License",
    ],
    cmdclass={
        "test": TestCommand,
    },
    setup_requires=["setuptools_scm"],
    use_scm_version={"version_scheme": version_scheme, "local_scheme": local_version},
    project_urls={
        "Documentation": "https://palewi.re/docs/django-yamlfield/",
        "Source": "https://github.com/datadesk/django-yamlfield/",
        "Tracker": "https://github.com/datadesk/django-yamlfield/issues",
    },
)
