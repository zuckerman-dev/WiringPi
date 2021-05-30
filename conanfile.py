from conans import ConanFile, CMake

class WiringPiConan(ConanFile):
   name = "WiringPi"
   version = "2.60.0"
   settings = "os", "compiler", "build_type", "arch"
   generators = "cmake", "gcc", "txt", "cmake_find_package"
   default_options = {}
   exports_sources = "*"

   @property
   def _source_subfolder(self):
      return "source_subfolder"
      
   def build(self):
      cmake = CMake(self)
      cmake.configure()
      cmake.build()   
      
   def imports(self):
      self.copy("*.dll", dst="bin", src="bin") # From bin to bin
      self.copy("*.dylib*", dst="bin", src="lib") # From lib to bin
      