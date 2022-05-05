################################################################################
# Package: xAHplusCPalgsExample
################################################################################

# Declare the package name:
atlas_subdir( xAHplusCPalgsExample )

# Find the needed external(s):
find_package( ROOT COMPONENTS Hist Tree )

# build a dictionary for the library
atlas_add_root_dictionary ( xAHplusCPalgsExample xAHplusCPalgsExampleDictSource
                            ROOT_HEADERS xAHplusCPalgsExample/*.h Root/LinkDef.h
                            EXTERNAL_PACKAGES ROOT
)


# build a shared library
atlas_add_library( xAHplusCPalgsExample
                   xAHplusCPalgsExample/*.h Root/*.h Root/*.cxx ${xAHplusCPalgsExampleDictSource}
		   PUBLIC_HEADERS xAHplusCPalgsExample
                   INCLUDE_DIRS ${ROOT_INCLUDE_DIRS}
                   LINK_LIBRARIES ${ROOT_LIBRARIES} EventLoop xAODRootAccess 
                   xAODEventInfo
                   xAODJet xAODMuon xAODParticleEvent
                   xAODAnaHelpersLib 
                   SystematicsHandlesLib
                   AsgTestingLib
                   SelectionHelpersLib
                   )

# Install files from the package:
#atlas_install_python_modules( configs/*.py )
atlas_install_python_modules( python/*.py )
atlas_install_scripts( scripts/*.sh )
