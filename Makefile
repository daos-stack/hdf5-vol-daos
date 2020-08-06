NAME          := hdf5-vol-daos
SRC_EXT       := bz2
TEST_PACKAGES := $(NAME) $(NAME)-mpich-tests $(NAME)-openmpi3-tests

include packaging/Makefile_packaging.mk
