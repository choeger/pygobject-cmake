set(_gobject_sources
        "gi/_gobject/gobjectmodule.c"
        "gi/_gobject/pygboxed.c"
        "gi/_gobject/pygboxed.h"
        "gi/_gobject/pygenum.c"
        "gi/_gobject/pygenum.h"
        "gi/_gobject/pygflags.c"
        "gi/_gobject/pygflags.h"
        "gi/_gobject/pyginterface.c"
        "gi/_gobject/pyginterface.h"
        "gi/_gobject/pygobject.c"
        "gi/_gobject/pygobject.h"
        "gi/_gobject/pygobject-private.h"
        "gi/_gobject/pygparamspec.c"
        "gi/_gobject/pygparamspec.h"
        "gi/_gobject/pygpointer.c"
        "gi/_gobject/pygpointer.h"
        "gi/_gobject/pygtype.c"
        "gi/_gobject/pygtype.h"
		)
		
include_directories(gi/_gobject gi/_glib gi/ ${GI_INCLUDE_DIRS} ${PYTHON_INCLUDE_DIRS} ${GLIB_INCLUDE_DIRS})

add_library(_gobject SHARED ${_gobject_sources})
target_link_libraries(_gobject pyglib_gi_2_0_${PYTHON_BASENAME} ${PYTHON_LIBRARIES} ${GLIB_LIBRARIES} ${GI_LIBRARIES})

set_target_properties(_gobject
 PROPERTIES
   PREFIX "" # There is no prefix even on UNIXes
   SUFFIX "${_modsuffix}" # The extension got from Python libraries
)