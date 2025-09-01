from importlib.metadata import PackageNotFoundError, version

pkg_name = 'imgkit'

try:
    pkg_version = version(pkg_name)
    __version__ = pkg_version
except PackageNotFoundError:
    print('Package not found!!')
    __version__ = '0.0.0'

