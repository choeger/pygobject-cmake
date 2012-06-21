add_definitions(-DPY_SSIZE_T_CLEAN)

set(pyglib_gi_2_0_${PYTHON_BASENAME}_sources
	"gi/_glib/pyglib.c"
	"gi/_glib/pyglib.h"
	"gi/_glib/pyglib-private.h"
	"gi/_glib/pyglib-python-compat.h"
	)

add_library(pyglib_gi_2_0_${PYTHON_BASENAME} SHARED ${pyglib_gi_2_0_${PYTHON_BASENAME}_sources})
target_link_libraries(pyglib_gi_2_0_${PYTHON_BASENAME} ${PYTHON_LIBRARIES} ${GLIB_LIBRARIES})

set_target_properties(pyglib_gi_2_0_${PYTHON_BASENAME}
 PROPERTIES
   PREFIX "" # There is no prefix even on UNIXes
   SUFFIX "${_modsuffix}" # The extension got from Python libraries
)

set(_glib_sources 
	"gi/_glib/glibmodule.c"
	"gi/_glib/pygiochannel.c"
	"gi/_glib/pygiochannel.h"
	"gi/_glib/pygoptioncontext.c"
	"gi/_glib/pygoptioncontext.h"
	"gi/_glib/pygoptiongroup.c"
	"gi/_glib/pygoptiongroup.h"
	"gi/_glib/pygmaincontext.c"
	"gi/_glib/pygmaincontext.h"
	"gi/_glib/pygmainloop.c"
	"gi/_glib/pygmainloop.h"
	"gi/_glib/pygsource.c"
	"gi/_glib/pygsource.h"
	"gi/_glib/pygspawn.c"
	"gi/_glib/pygspawn.h"
	)

include_directories(gi/_glib ${PYTHON_INCLUDE_DIRS} ${GLIB_INCLUDE_DIRS})

add_library(_glib SHARED ${_glib_sources})
target_link_libraries(_glib pyglib_gi_2_0_${PYTHON_BASENAME} ${PYTHON_LIBRARIES} ${GLIB_LIBRARIES})

set_target_properties(_glib
 PROPERTIES
   PREFIX "" # There is no prefix even on UNIXes
   SUFFIX "${_modsuffix}" # The extension got from Python libraries
)
