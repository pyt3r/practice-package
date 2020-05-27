import os.path


def _get_version():
    from pkg_resources import get_distribution, DistributionNotFound
    here = os.path.dirname(__file__)
    package = os.path.basename(here)

    try:
        version = get_distribution(package).version
    except DistributionNotFound:
        version = here
    return version


__version__ = _get_version()


def getResourceManifest():
    """
    gets the Resource Manifest

    Returns
    -------
    basename: str
    filename: str
    manifest: dict
    """
    import yaml
    here = os.path.abspath(os.path.dirname(__file__))
    basename = os.path.basename(here)
    filename = 'manifest.yaml'
    manifest = yaml.load(
        open(
            os.path.join(
                here,
                filename),
            'rb'),
        Loader=yaml.SafeLoader)
    return basename, filename, manifest


def dumpResourceManifest():
    """
    dumps the Resource Manifest to a dictionary form

    Returns
    -------
    manifest object : dict

        manifest object with the following structure:

          package_data:
              [path]: [filename1, filename2, ...]

          unpackage_data:
              [path]: [filename1, filename2, ...]

    """
    import os.path
    basename, filename, manifest = getResourceManifest()

    package_data = {basename: [filename], }
    for package_name, body in manifest['package_data'].items():
        arr = []
        for filepath, filenames in body.items():
            arr.extend([os.path.join(filepath, f) for f in filenames])
        package_data[package_name] = package_data.get(package_name, []) + arr
    return package_data
