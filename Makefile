NAME             := hdf5-vol-daos
SRC_EXT          := gz
TEST_PACKAGES    := daos-devel $(NAME) $(NAME)-mpich $(NAME)-openmpi3 $(NAME)-mpich-devel $(NAME)-openmpi3-devel $(NAME)-mpich-tests $(NAME)-openmpi3-tests
SOURCE_VERSION   := 1.1.0rc1
TEST_VERSION     := 0.9.0
SOURCE           := v$(SOURCE_VERSION).tar.$(SRC_EXT)
PATCHES          := v$(TEST_VERSION).tar.$(SRC_EXT)
BUILD_DEFINES    := --define "%source_version $(SOURCE_VERSION)" --define "%test_version $(TEST_VERSION)"
RPM_BUILD_OPTIONS := $(BUILD_DEFINES)

v$(SOURCE_VERSION).tar.$(SRC_EXT):
       curl -f -L -O https://github.com/HDFGroup/vol-daos/archive/v$(SOURCE_VERSION).tar.$(SRC_EXT)

v$(TEST_VERSION).tar.$(SRC_EXT):
       curl -f -L -O https://github.com/HDFGroup/vol-tests/archive/v$(TEST_VERSION).tar.$(SRC_EXT)

include packaging/Makefile_packaging.mk
