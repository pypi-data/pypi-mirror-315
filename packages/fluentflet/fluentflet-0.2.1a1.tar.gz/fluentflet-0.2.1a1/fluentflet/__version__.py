VERSION_MAJOR = 0
VERSION_MINOR = 2
VERSION_PATCH = 1
VERSION_INFO = (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)

VERSION_STATUS = "alpha"  # "alpha", "beta", "rc", "final"
VERSION_BUILD = 1

# full version string
VERSION = f"{'.'.join(map(str, VERSION_INFO))}"
if VERSION_STATUS != "final":
    VERSION += f"{VERSION_STATUS}{VERSION_BUILD}"
