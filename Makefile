NAME    := hdf5-vol-daos
SRC_EXT := gz
TEST_PACKAGES := daos-devel $(NAME) $(NAME)-mpich $(NAME)-openmpi3 $(NAME)-mpich-devel $(NAME)-openmpi3-devel $(NAME)-mpich-tests $(NAME)-openmpi3-tests

include source_deps.mk

include packaging/Makefile_packaging.mk

source_deps.mk:
	for s in $(SOURCES); do \
		echo $${s##*/}:; \
	done > $@
