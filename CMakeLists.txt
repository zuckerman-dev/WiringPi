cmake_minimum_required(VERSION 3.10)

project(WiringPi VERSION 2.60.0)

include(GNUInstallDirs)

set(HEADERS 
    wiringPi/ads1115.h
    wiringPi/bmp180.h
    wiringPi/drcNet.h
    wiringPi/drcSerial.h
    wiringPi/ds18b20.h
    wiringPi/htu21d.h
    wiringPi/max31855.h
    wiringPi/max5322.h
    wiringPi/mcp23008.h
    wiringPi/mcp23016.h
    wiringPi/mcp23017.h
    wiringPi/mcp23016reg.h
    wiringPi/mcp23s08.h
    wiringPi/mcp23s17.h
    wiringPi/mcp23x0817.h
    wiringPi/mcp23x08.h
    wiringPi/mcp3004.h
    wiringPi/mcp3002.h
    wiringPi/mcp3422.h
    wiringPi/mcp4802.h
    wiringPi/pcf8574.h
    wiringPi/pcf8591.h
    wiringPi/pseudoPins.h
    wiringPi/rht03.h
    wiringPi/sn3218.h
    wiringPi/softPwm.h
    wiringPi/softTone.h
    wiringPi/sr595.h
    wiringPi/wiringPi.h
    wiringPi/wiringPiI2C.h
    wiringPi/wiringPiSPI.h
    wiringPi/wiringSerial.h
    wiringPi/wiringShift.h
    wiringPi/wpiExtensions.h
    wiringPi/softServo.h
)

set(SRC 
    wiringPi/ads1115.c
    wiringPi/bmp180.c
    wiringPi/COPYING.LESSER
    wiringPi/drcNet.c
    wiringPi/drcSerial.c
    wiringPi/ds18b20.c
    wiringPi/htu21d.c
    wiringPi/max31855.c
    wiringPi/max5322.c
    wiringPi/mcp23008.c
    wiringPi/mcp23016.c
    wiringPi/mcp23017.c
    wiringPi/mcp23s08.c
    wiringPi/mcp23s17.c
    wiringPi/mcp3002.c
    wiringPi/mcp3004.c
    wiringPi/mcp3422.c
    wiringPi/mcp4802.c
    wiringPi/noMoreStatic
    wiringPi/pcf8574.c
    wiringPi/pcf8591.c
    wiringPi/piHiPri.c
    wiringPi/piThread.c
    wiringPi/pseudoPins.c
    wiringPi/rht03.c
    wiringPi/sn3218.c
    wiringPi/softPwm.c
    wiringPi/softServo.c
    wiringPi/softTone.c
    wiringPi/sr595.c
    wiringPi/wiringPi.c
    wiringPi/wiringPiI2C.c
    wiringPi/wiringPiSPI.c
    wiringPi/wiringSerial.c
    wiringPi/wiringShift.c
    wiringPi/wpiExtensions.c
)

set(DAEMON_SRC 
    wiringPiD/daemonise.c
    wiringPiD/network.c
    wiringPiD/runRemote.c
    wiringPiD/wiringpid.c
)

set(DEVLIB_HEADERS 
    devLib/ds1302.h
    devLib/font.h
    devLib/gertboard.h
    devLib/lcd128x64.h
    devLib/lcd.h
    devLib/maxdetect.h
    devLib/piFace.h
    devLib/piGlow.h
    devLib/piNes.h
    devLib/scrollPhatFont.h
    devLib/scrollPhat.h
)

set(DEV_SRC 
    devLib/ds1302.c
    devLib/gertboard.c
    devLib/lcd128x64.c
    devLib/lcd.c
    devLib/maxdetect.c
    devLib/piFace.c
    devLib/piGlow.c
    devLib/piNes.c
    devLib/scrollPhat.c
)

find_package(PkgConfig REQUIRED)
find_package(Threads REQUIRED)

pkg_check_modules(gcrypt QUIET REQUIRED IMPORTED_TARGET "libgcrypt")

add_library(${PROJECT_NAME} SHARED ${SRC})
add_library(${PROJECT_NAME}Dev SHARED ${DEV_SRC})

target_link_libraries(${PROJECT_NAME}Dev PUBLIC ${PROJECT_NAME} crypt m rt)
target_include_directories(${PROJECT_NAME}Dev
    PRIVATE 
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/wiringPi>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/devLib>
    )
set_property(TARGET ${PROJECT_NAME}Dev PROPERTY VERSION ${PROJECT_VERSION})
set_property(TARGET ${PROJECT_NAME}Dev PROPERTY SOVERSION ${PROJECT_VERSION_MAJOR})

install(TARGETS ${PROJECT_NAME}Dev DESTINATION ${CMAKE_INSTALL_LIBDIR})
install(FILES ${DEVLIB_HEADERS} DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/${PROJECT_NAME}/${PROJECT_VERSION_MAJOR}/dev/)

target_link_libraries(${PROJECT_NAME} PUBLIC PkgConfig::gcrypt)

set_property(TARGET ${PROJECT_NAME} PROPERTY VERSION ${PROJECT_VERSION})
set_property(TARGET ${PROJECT_NAME} PROPERTY SOVERSION ${PROJECT_VERSION_MAJOR})

target_include_directories(${PROJECT_NAME} 
    PRIVATE $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/wiringPi>
    PUBLIC $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}/${PROJECT_NAME}/${PROJECT_VERSION_MAJOR}/>)

add_executable(wiringpi-gpio gpio/gpio.c gpio/readall.c)
target_link_libraries(wiringpi-gpio ${PROJECT_NAME} ${PROJECT_NAME}Dev Threads::Threads rt crypt m)
target_include_directories(wiringpi-gpio
    PRIVATE 
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/wiringPiD>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/wiringPi>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/gpio>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/devLib>
        )

add_executable(wiringpid ${DAEMON_SRC})
target_link_libraries(wiringpid ${PROJECT_NAME} Threads::Threads rt crypt m)
install(TARGETS wiringpid DESTINATION ${CMAKE_INSTALL_BINDIR})
target_include_directories(wiringpid
    PRIVATE 
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/wiringPiD>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/wiringPi>)

include(CMakePackageConfigHelpers)

install(TARGETS ${PROJECT_NAME} 
    EXPORT ${PROJECT_NAME}Targets
    DESTINATION ${CMAKE_INSTALL_LIBDIR}
    )

write_basic_package_version_file(
  "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}/${PROJECT_NAME}ConfigVersion.cmake"
  VERSION ${PROJECT_VERSION}
  COMPATIBILITY AnyNewerVersion
)

configure_package_config_file(${PROJECT_NAME}Config.cmake.in
  ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}/${PROJECT_NAME}Config.cmake
  INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}/)

install(EXPORT ${PROJECT_NAME}Targets
  FILE
    ${PROJECT_NAME}Targets.cmake
  NAMESPACE "${PROJECT_NAME}::"
  DESTINATION
    ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}
  COMPONENT
    Devel
)
  
install(
  FILES
    "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}/${PROJECT_NAME}Config.cmake"
    "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}/${PROJECT_NAME}ConfigVersion.cmake"
  DESTINATION
    ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}
  COMPONENT
    Devel
)

install(FILES ${HEADERS} 
    DESTINATION 
        ${CMAKE_INSTALL_INCLUDEDIR}/WiringPi/${PROJECT_VERSION_MAJOR}/
    COMPONENT 
        Devel
    )