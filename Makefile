NAME          := hdf5-vol-daos
SRC_EXT       := gz
TEST_PACKAGES := daos-devel $(NAME) $(NAME)-mpich $(NAME)-openmpi3 $(NAME)-mpich-devel $(NAME)-openmpi3-devel $(NAME)-mpich-tests $(NAME)-openmpi3-tests
VOL_MAJOR     := 1
VOL_MINOR     := 1
VOL_RELEASE   := 0rc1
TEST_COMMIT   := c6d8c31e14e7d43f3b02f8906e8ecab2726e76ba
PATCHES       := $(TEST_COMMIT).tar.$(SRC_EXT)
BUILD_DEFINES := --define "%vol_major $(VOL_MAJOR)"  --define "%vol_minor $(VOL_MINOR)"  --define "%vol_release $(VOL_RELEASE)" --define "%test_commit $(TEST_COMMIT)"
RPM_BUILD_OPTIONS := $(BUILD_DEFINES)
DL_VERSION    := vol-daos-$(VOL_MAJOR).$(VOL_MINOR).$(VOL_RELEASE)

include packaging/Makefile_packaging.mk

$(TEST_COMMIT).tar.$(SRC_EXT):
       curl -f -L -O https://github.com/HDFGroup/vol-tests/archive/$(TEST_COMMIT).tar.$(SRC_EXT)
