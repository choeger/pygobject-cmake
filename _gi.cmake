set(_gi_sources
	"gi/pygi-repository.c"
	"gi/pygi-repository.h"
	"gi/pygi-info.c"
	"gi/pygi-info.h"
	"gi/pygi-foreign.c"
	"gi/pygi-foreign.h"
	"gi/pygi-foreign-gvariant.c"
	"gi/pygi-foreign-gvariant.h"
	"gi/pygi-struct.c"
	"gi/pygi-struct.h"
	"gi/pygi-argument.c"
	"gi/pygi-argument.h"
	"gi/pygi-type.c"
	"gi/pygi-type.h"
	"gi/pygi-boxed.c"
	"gi/pygi-boxed.h"
	"gi/pygi-closure.c"
	"gi/pygi-closure.h"
	"gi/pygi-ccallback.c"
	"gi/pygi-ccallback.h"
	"gi/pygi-callbacks.c"
	"gi/pygi-callbacks.h"
	"gi/pygi.h"
	"gi/pygi-private.h"
	"gi/pygi-property.c"
	"gi/pygi-property.h"
	"gi/pygi-signal-closure.c"
	"gi/pygi-signal-closure.h"
	"gi/pygobject-external.h"
	"gi/gimodule.c"
	"gi/pygi-invoke.c"
	"gi/pygi-invoke.h"
	"gi/pygi-invoke-state-struct.h"
	"gi/pygi-cache.h"
	"gi/pygi-cache.c"
	"gi/pygi-marshal-from-py.c"
	"gi/pygi-marshal-from-py.h"
	"gi/pygi-marshal-to-py.c"
	"gi/pygi-marshal-to-py.h"
	"gi/pygi-marshal-cleanup.c"
	"gi/pygi-marshal-cleanup.h"
	)
	
include_directories(${FFI_INCLUDE_DIRS} gi/_gobject gi/_glib gi/ ${PYTHON_INCLUDE_DIRS} ${GLIB_INCLUDE_DIRS})

add_library(_gi SHARED ${_gi_sources})
target_link_libraries(_gi pyglib_gi_2_0_${PYTHON_BASENAME} ${PYTHON_LIBRARIES} ${GLIB_LIBRARIES} ${GI_LIBRARIES})

set_target_properties(_gi
 PROPERTIES
   PREFIX "" # There is no prefix even on UNIXes
   SUFFIX "${_modsuffix}" # The extension got from Python libraries
)