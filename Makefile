NAME             := hdf5-vol-daos
SRC_EXT          := gz
TEST_PACKAGES    := daos-devel $(NAME) $(NAME)-mpich $(NAME)-openmpi3 $(NAME)-mpich-devel $(NAME)-openmpi3-devel $(NAME)-mpich-tests $(NAME)-openmpi3-tests
SOURCE_VERSION   := v1.1.0rc1
TEST_VERSION     := v0.9.0
SOURCE           := $(SOURCE_VERSION).tar.$(SRC_EXT)
PATCHES          := $(TEST_VERSION).tar.$(SRC_EXT)
BUILD_DEFINES    := --define "%source_version $(SOURCE_VERSION)" --define "%test_version $(TEST_VERSON)"
RPM_BUILD_OPTIONS := $(BUILD_DEFINES)


$(SOURCE_VERSION).tar.$(SRC_EXT):
       curl -f -L -O https://github.com/HDFGroup/vol-daos/archive/v$(VOL_MAJOR).$(VOL_MINOR).$(VOL_RELEASE).tar.$(SRC_EXT)

$(TEST_VERSION).tar.$(SRC_EXT):
       curl -f -L -O https://github.com/HDFGroup/vol-tests/archive/v$(TEST_VERSION).tar.$(SRC_EXT)

include packaging/Makefile_packaging.mk
