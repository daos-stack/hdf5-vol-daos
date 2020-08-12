NAME          := hdf5-vol-daos
SRC_EXT       := gz
TEST_PACKAGES := $(NAME) $(NAME)-mpich $(NAME)-openmpi3 $(NAME)-mpich-devel $(NAME)-openmpi3-devel $(NAME)-mpich-tests $(NAME)-openmpi3-tests
SOURCE_COMMIT := b324b90d4554e211976174b9a3acdba61c184248
TEST_COMMIT   := 31660ab19352049cf59f98b1fba498b3e93dade5
SOURCE        := $(SOURCE_COMMIT).tar.$(SRC_EXT)
GIT_SHORT     := $(shell git rev-parse --short $(SOURCE_COMMIT))
BUILD_DEFINES := --define "%relval .g$(GIT_SHORT)" --define "%source_commit $(SOURCE_COMMIT)" --define "%test_commit $(TEST_COMMIT)"

include packaging/Makefile_packaging.mk
