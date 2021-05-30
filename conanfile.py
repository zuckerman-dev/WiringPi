from conans import ConanFile, CMake

class WiringPiConan(ConanFile):
   name = "WiringPi"
   version = "2.60.0"
   settings = "os", "compiler", "build_type", "arch"
   generators = "cmake", "gcc", "txt", "cmake_find_package"
   default_options = {}

   scm = {
      "type" : "git",
      "subfolder" : ".",
      "url" : "https://github.com/zuckerman-dev/WiringPi.git",
      "revision" : "auto", 
      "submodule" : "recursive"
   }
   no_copy_source = True
   keep_imports = True
   
   def build(self):
      cmake = CMake(self)
      cmake.configure()
      cmake.build()   
      
   def imports(self):
      self.copy("*.dll", dst="bin", src="bin") # From bin to bin
      self.copy("*.dylib*", dst="bin", src="lib") # From lib to bin
      