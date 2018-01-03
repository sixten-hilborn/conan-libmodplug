from conans import ConanFile, CMake
from conans.tools import download, unzip
import os
import shutil

class LibmodplugConan(ConanFile):
    name = "libmodplug"
    version = "0.8.8.5"
    description = "libmodplug plays mod-like music formats"
    folder = "libmodplug-%s" % version
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False]
    }
    default_options = (
        'shared=False',
        'fPIC=True'
    )
    generators = "cmake"
    exports = ["CMakeLists.txt"]
    url = "https://github.com/sixten-hilborn/conan-libmodplug"
    license = "Public Domain"


    def source(self):
        zip_name = "%s.tar.gz" % self.folder
        download("http://sourceforge.net/projects/modplug-xmms/files/{0}/{1}/{2}/download".format(self.name, self.version, zip_name), zip_name)
        unzip(zip_name)
        os.unlink(zip_name)
        shutil.move("CMakeLists.txt", "%s/CMakeLists.txt" % self.folder)

    def build(self):
        cmake = CMake(self)
        defs = {
            'CMAKE_INSTALL_PREFIX': os.path.join(self.conanfile_directory, 'install'),
            'CMAKE_POSITION_INDEPENDENT_CODE': self.options.fPIC,
            'BUILD_SHARED_LIBS': self.options.shared
        }
        src = os.path.join(self.conanfile_directory, self.folder)
        cmake.configure(build_dir='build', source_dir=src, defs=defs)
        cmake.build(target='install')

    def package(self):
        """ Define your conan structure: headers, libs and data. After building your
            project, this method is called to create a defined structure:
        """
        folder = 'install'
        self.copy(pattern="*.h", dst="include", src=folder, keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src=folder, keep_path=False)
        self.copy(pattern="*.dll*", dst="bin", src=folder, keep_path=False)
        self.copy(pattern="*.a", dst="lib", src=folder, keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src=folder, keep_path=False)
        self.copy(pattern="*.dylib*", dst="lib", src=folder, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["modplug"]
