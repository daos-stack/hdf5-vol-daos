NAME          := hdf5-vol-daos
SRC_EXT       := gz
TEST_PACKAGES := daos-devel $(NAME) $(NAME)-mpich $(NAME)-openmpi3 $(NAME)-mpich-devel $(NAME)-openmpi3-devel $(NAME)-mpich-tests $(NAME)-openmpi3-tests
DEB_SOURCE    := hdf5-vol-daos+vol-tests.tar.gz

include source_deps.mk

include packaging/Makefile_packaging.mk

source_deps.mk:$(notdir $(SOURCES))
	for s in $(notdir $(SOURCES)); do \
		echo $$s:;                 \
	done > $@

ifeq ($(ID_LIKE),debian)
$(SOURCE): $(notdir $(REAL_SOURCE)) $(OTHER_SOURCES)
	rm -rf $(subst .tar.gz,,$@)
	mkdir $(subst .tar.gz,,$@)
	tar -C $(subst .tar.gz,,$@) --strip 1 -xf $(notdir $(REAL_SOURCE))
	tar -C $(subst .tar.gz,,$@)/test/vol --strip 1 -xf $(OTHER_SOURCES)
	tar -czf $@ $(subst .tar.gz,,$@)
	rm -rf $(subst .tar.gz,,$@)
endif
