NAME          := hdf5-vol-daos
SRC_EXT       := zip
TEST_PACKAGES := $(NAME) $(NAME)-mpich-tests $(NAME)-openmpi3-tests

include packaging/Makefile_packaging.mk
