NAME          := hdf5-vol-daos
SRC_EXT       := gz
TEST_PACKAGES := daos-devel $(NAME) $(NAME)-mpich $(NAME)-openmpi3 $(NAME)-mpich-devel $(NAME)-openmpi3-devel $(NAME)-mpich-tests $(NAME)-openmpi3-tests
SOURCE_COMMIT := 8d419310976bcd890521ebf72557325f34a8af56
TEST_COMMIT   := d59811a39cd5053887f22cdabd1c08e6d9c539db
SOURCE        = $(SOURCE_COMMIT).tar.$(SRC_EXT) 
PATCHES       = $(TEST_COMMIT).tar.$(SRC_EXT)
GIT_SHORT     := $(shell git rev-parse --short $(SOURCE_COMMIT))
BUILD_DEFINES := --define "%relval .g$(GIT_SHORT)" --define "%source_commit $(SOURCE_COMMIT)" --define "%test_commit $(TEST_COMMIT)"
RPM_BUILD_OPTIONS := $(BUILD_DEFINES)

$(SOURCE_COMMIT).tar.$(SRC_EXT):
	curl -f -L -O https://github.com/HDFGroup/vol-daos/archive/$(SOURCE_COMMIT).tar.$(SRC_EXT)

$(TEST_COMMIT).tar.$(SRC_EXT):
	curl -f -L -O https://github.com/HDFGroup/vol-tests/archive/$(TEST_COMMIT).tar.$(SRC_EXT)

include packaging/Makefile_packaging.mk
