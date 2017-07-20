from conan.packager import ConanMultiPackager
from conans.tools import os_info

if __name__ == "__main__":
    builder = ConanMultiPackager()
    builder.add_common_builds(shared_option_name="libmodplug:shared", pure_c=False)
    builder.run()
