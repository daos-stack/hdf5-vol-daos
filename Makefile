NAME          := hdf5-vol-daos
SRC_EXT       := gz
TEST_PACKAGES := daos-devel $(NAME) $(NAME)-mpich $(NAME)-openmpi3 $(NAME)-mpich-devel $(NAME)-openmpi3-devel $(NAME)-mpich-tests $(NAME)-openmpi3-tests
VOL_MAJOR     := 1
VOL_MINOR     := 1
VOL_RELEASE   := 0rc1
TEST_VERSION  := 0.9.0
BUILD_DEFINES := --define "%test_version $(TEST_VERSION)" --define "%vol_major $(VOL_MAJOR)"  --define "%vol_minor $(VOL_MINOR)"  --define "%vol_release $(VOL_RELEASE)"
RPM_BUILD_OPTIONS := $(BUILD_DEFINES)
DL_VERSION    := vol-daos-$(VOL_MAJOR).$(VOL_MINOR).$(VOL_RELEASE)
PATCHES       := vol-tests-$(TEST_VERSION)

vol-daos-$(VOL_MAJOR).$(VOL_MINOR).$(VOL_RELEASE).tar.$(SRC_EXT):
       curl -f -L -O https://github.com/HDFGroup/vol-daos/archive/v$(VOL_MAJOR).$(VOL_MINOR).$(VOL_RELEASE).tar.$(SRC_EXT)

vol-tests-$(TEST_VERSION).tar.$(SRC_EXT):
       curl -f -L -O https://github.com/HDFGroup/vol-tests/archive/v$(TEST_VERSION).tar.$(SRC_EXT)

include packaging/Makefile_packaging.mk