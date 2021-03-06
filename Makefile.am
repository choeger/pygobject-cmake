ACLOCAL_AMFLAGS = -I m4 ${ACLOCAL_FLAGS}
AUTOMAKE_OPTIONS = 1.7

SUBDIRS = examples gi tests

PLATFORM_VERSION = 3.0

CLEANFILES = \
	`find "$(builddir)" -type f -name "*.pyc" -print`

EXTRA_DIST = \
	ChangeLog.pre-2.18 \
	pygobject-$(PLATFORM_VERSION).pc.in \
	PKG-INFO \
	PKG-INFO.in \
	m4/as-ac-expand.m4 \
	m4/jhflags.m4 \
	m4/python.m4

MAINTAINERCLEANFILES = \
	$(srcdir)/INSTALL \
	$(srcdir)/aclocal.m4 \
	$(srcdir)/autoscan.log \
	$(srcdir)/compile \
	$(srcdir)/config.guess \
	$(srcdir)/config.h.in \
	$(srcdir)/config.sub \
	$(srcdir)/configure.scan \
	$(srcdir)/depcomp \
	$(srcdir)/install-sh \
	$(srcdir)/ltmain.sh \
	$(srcdir)/missing \
	$(srcdir)/mkinstalldirs \
	$(srcdir)/omf.make \
	$(srcdir)/xmldocs.make \
	$(srcdir)/gtk-doc.make \
	$(srcdir)/ChangeLog \
	$(srcdir)/py-compile \
	$(srcdir)/m4/libtool.m4 \
	$(srcdir)/m4/ltoptions.m4 \
	$(srcdir)/m4/ltsugar.m4 \
	$(srcdir)/m4/ltversion.m4 \
	$(srcdir)/m4/lt~obsolete.m4 \
	`find "$(srcdir)" -type f -name Makefile.in -print` \
	`find "$(builddir)" -type f -name "*.pyc" -print`

BUILT_EXTRA_DIST = 		\
	ChangeLog

# pkg-config files
pkgconfigdir = $(libdir)/pkgconfig
pkgconfig_DATA = pygobject-$(PLATFORM_VERSION).pc

# python
pyexec_LTLIBRARIES =

# install pth file.
install-data-local:
	$(mkinstalldirs) $(DESTDIR)$(pythondir)
install-exec-local:
	$(mkinstalldirs) $(DESTDIR)$(pyexecdir)
uninstall-local:

EGG_NAME = $(PACKAGE)-$(PACKAGE_VERSION)-py$(PYTHON_VERSION)-$(PLATFORM).egg

egg: EGG_TMPDIR:=$(TMPDIR)/$(PACKAGE)-$(PACKAGE_VERSION)
egg: $(top_srcdir)/gobject/gobject.la PKG-INFO
	rm -fr $(EGG_TMPDIR)
	echo $(EGG_NAME)
	$(MKDIR_P) $(EGG_TMPDIR)
	$(MKDIR_P) $(EGG_TMPDIR)/EGG-INFO
	$(MAKE) -C gobject install-pkgpyexecLTLIBRARIES pkgpyexecdir=$(EGG_TMPDIR)
	rm -fr $(EGG_TMPDIR)/gobject.la
	$(INSTALL) PKG-INFO $(EGG_TMPDIR)/EGG-INFO
	echo "gobject.so" >> $(EGG_TMPDIR)/EGG-INFO/native_libs.txt
	( echo "gobject" ) >> $(EGG_TMPDIR)/EGG-INFO/top_level.txt
	cd $(EGG_TMPDIR) && zip -rq $(EGG_NAME) .
	mv $(EGG_TMPDIR)/$(EGG_NAME) .
	rm -fr $(EGG_TMPDIR)

doc-dist:
	mkdir pygobject
	cp -r docs/html/*.html pygobject
	cp -r docs/html/*.sgml pygobject
	cp -r docs/html/*.devhelp pygobject
	cp -r docs/style.css pygobject
	tar cfz $(PACKAGE)-docs.tar.gz pygobject
	rm -fr pygobject

release-tag:
	@ROOT=`svn info --xml|egrep ^"<url>"|cut -d\> -f2|cut -d\< -f1`; \
	SVNVERSION=`echo $(VERSION)|sed s/\\\./_/g`;\
	  echo "* Tagging $(VERSION)"; \
          svn cp -m "Tag $(VERSION)" \
              $$ROOT \
              svn+ssh://johan@svn.gnome.org/svn/pygobject/tags/PYGOBJECT_$$SVNVERSION

release-news:
	printf "%-8s%s\n" "$(VERSION)" "`LC_TIME=C date '+%d-%b-%Y'`" > NEWS.tmp
	last=`head -n1 NEWS | cut -f1 -d' '`; \
	git log --format='format:        - %s (%aN)%n%b' $$last.. | \
	  sed -n '/^        -/ p; /bugzilla.gnome.org/ { s/^.*id=\([0-9]\+\).*$$/          (#\1)/; p}' >> NEWS.tmp
	echo >> NEWS.tmp
	cat NEWS >> NEWS.tmp
	mv NEWS.tmp NEWS

.PHONY: ChangeLog release-news

ChangeLog:
	@echo Creating $@
	@if test -d "$(srcdir)/.git"; then \
	  (GIT_DIR=$(top_srcdir)/.git ./missing --run git log PYGOBJECT_2_17_0^^.. --stat) | fmt --split-only > $@.tmp \
	  && mv -f $@.tmp $@ \
	  || ($(RM) $@.tmp; \
	      echo Failed to generate ChangeLog, your ChangeLog may be outdated >&2; \
	      (test -f $@ || echo git-log is required to generate this file >> $@)); \
	else \
	  test -f $@ || \
	  (echo A git checkout and git-log is required to generate ChangeLog >&2 && \
	  echo A git checkout and git-log is required to generate this file >> $@); \
	fi


distclean-local:
	if test $(srcdir) = .; then :; else \
	    rm -f $(BUILT_EXTRA_DIST); \
	fi

dist-hook: $(BUILT_EXTRA_DIST)
	files='$(BUILT_EXTRA_DIST)'; \
	for f in $$files; do \
	  if test -f $$f; then d=.; else d=$(srcdir); fi; \
	  rm -f $(distdir)/$$f && cp $$d/$$f $(distdir) || exit 1; done

check.gdb:
	cd tests && $(MAKE) check.gdb

check.nemiver:
	cd tests && $(MAKE) check.nemiver

check.valgrind:
	cd tests && $(MAKE) check.valgrind


-include $(top_srcdir)/git.mk
