
find_library(GIREPO_LIBRARY NAMES girepository_1_0)

find_path(GI_INCLUDE_DIR NAMES girepository.h PATH_SUFFIXES gobject-introspection-1.0)

if (GI_INCLUDE_DIR AND GIREPO_LIBRARY)
    set(GI_INCLUDE_DIRS ${GI_INCLUDE_DIR})
	set(GI_LIBRARIES ${GIREPO_LIBRARY})
    set(GI_FOUND TRUE)
else (GI_INCLUDE_DIR AND GIREPO_LIBRARY)
	set(GI_FOUND FALSE)
endif (GI_INCLUDE_DIR AND GIREPO_LIBRARY)

IF( GI_FOUND )
    MESSAGE( STATUS "Found gobject-introspection: ${GI_INCLUDE_DIRS} ${GI_LIBRARIES}" )
    ELSE( GI_FOUND )
    IF( GI_FIND_REQUIRED )
    	MESSAGE( FATAL_ERROR "Could not find gobject-introspection" )
    ENDIF( GI_FIND_REQUIRED )
ENDIF( GI_FOUND )

mark_as_advanced(GI_INCLUDE_DIR GI_INCLUDE_DIRS GI_LIBRARIES)