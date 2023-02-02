NAME          := hdf5-vol-daos
SRC_EXT       := gz
TEST_PACKAGES := daos-devel $(NAME) $(NAME)-mpich $(NAME)-openmpi3 $(NAME)-mpich-devel $(NAME)-openmpi3-devel $(NAME)-mpich-tests $(NAME)-openmpi3-tests
DEB_SOURCE    := hdf5-vol-daos+vol-tests.tar.gz

include packaging/Makefile_packaging.mk

ifeq ($(ID_LIKE),debian)
$(SOURCE): $(notdir $(REAL_SOURCE)) $(notdir $(OTHER_SOURCES))
	rm -rf $(subst .tar.gz,,$@)
	mkdir $(subst .tar.gz,,$@)
	tar -C $(subst .tar.gz,,$@) --strip 1 -xf $(notdir $(REAL_SOURCE))
	tar -C $(subst .tar.gz,,$@)/test/vol --strip 1 -xf $(notdir $(OTHER_SOURCES))
	tar -czf $@ $(subst .tar.gz,,$@)
	rm -rf $(subst .tar.gz,,$@)
endif
