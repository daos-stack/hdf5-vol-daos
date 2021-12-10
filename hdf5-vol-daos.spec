%global with_mpich 1
%if (0%{?rhel} >= 8)
%global with_openmpi 1
%global with_openmpi3 0
%else
%global with_openmpi 0
%global with_openmpi3 1
%endif

%global vol_test_tag 0.9.3
%global vol_major 1
%global vol_minor 1
%global vol_bugrelease 0
%global vol_prerelease rc4
%global vol_tag  %{vol_major}.%{vol_minor}.%{vol_bugrelease}%{?vol_prerelease:%{vol_prerelease}}

%if %{with_mpich}
%global mpi_list mpich
%endif
%if %{with_openmpi}
%global mpi_list %{?mpi_list} openmpi
%endif
%if %{with_openmpi3}
%global mpi_list %{?mpi_list} openmpi3
%endif

%if (0%{?suse_version} >= 1500)
%global module_load() if [ "%{1}" == "openmpi3" ]; then MODULEPATH=/usr/share/modules module load gnu-openmpi; else MODULEPATH=/usr/share/modules module load gnu-%{1}; fi
%else
%global module_load() module load mpi/%{1}-%{_arch}
%endif

%if (0%{?suse_version} >= 1500)
%global cmake cmake
%else
%global cmake cmake3
%endif

%if (0%{?suse_version} >= 1500)
%global mpi_libdir %{_libdir}/mpi/gcc
%global mpi_incldir  %{_includedir}/mpi/gcc
%else
%global mpi_libdir %{_libdir}
%global mpi_incldir  %{_includedir}
%endif

Name:    hdf5-vol-daos
Version: %{vol_major}.%{vol_minor}.%{vol_bugrelease}%{?vol_prerelease:~%{vol_prerelease}}
Release: 1%{?commit:.git%{shortcommit}}%{?dist}
Summary: A Multi-purpose, Application-Centric, Scalable I/O Proxy Application

License: GPL
URL: https://portal.hdfgroup.org/display/HDF5/HDF5
Source0: https://github.com/HDFGroup/vol-daos/archive/v%{vol_tag}.tar.gz
Source1: https://github.com/HDFGroup/vol-tests/archive/v%{vol_test_tag}.tar.gz

BuildRequires: daos-devel%{?_isa}
# Temporarily needed until daos-devel R: libuuid-devel
BuildRequires: libuuid-devel
# Should this be in daos-devel R: boost-devel?
BuildRequires: boost-devel
BuildRequires: gcc, gcc-c++
%if (0%{?suse_version} >= 1500)
BuildRequires: cmake >= 3.1
BuildRequires: lua-lmod
%else
BuildRequires: cmake3 >= 3.1
BuildRequires: Lmod
%endif
BuildRequires: hdf5-devel%{?_isa}
BuildRequires: libuuid-devel

%description
HDF5 VOL DAOS connector is used to leverage the
capabilities of the DAOS object storage system
within an HDF5 application.  It translates HDF5 VOL
storage related calls into native daos storage operations

%if %{with_openmpi}
%package openmpi
Summary: HDF5 VOL DAOS with OpenMPI 3
BuildRequires: hdf5-openmpi-devel%{?_isa} >= 1.12.1
Provides: %{name}-openmpi = %{version}-%{release}

%description openmpi
HDF5 VOL DAOS with OpenMPI 3

%package openmpi-devel
Summary: HDF5 VOL DAOS devel with OpenMPI 3
Requires: hdf5-openmpi-devel%{?_isa}
Requires: %{name}-openmpi%{?_isa} = %{version}-%{release}
Provides: %{name}-openmpi-devel = %{version}-%{release}

%description openmpi-devel
HDF5 VOL DAOS devel with OpenMPI 3

%package openmpi-tests
Summary: HDF5 VOL DAOS tests with openmpi
Requires: %{name}-openmpi%{?_isa} = %{version}-%{release}

%description openmpi-tests
HDF5 VOL DAOS tests with openmpi
%endif

%if %{with_openmpi3}
%package openmpi3
Summary: HDF5 VOL DAOS with OpenMPI 3
BuildRequires: hdf5-openmpi3-devel%{?_isa} >= 1.12.1
Provides: %{name}-openmpi3 = %{version}-%{release}

%description openmpi3
HDF5 VOL DAOS with OpenMPI 3

%package openmpi3-devel
Summary: HDF5 VOL DAOS devel with OpenMPI 3
Requires: hdf5-openmpi3-devel%{?_isa} >= 1.12.1
Requires: %{name}-openmpi3%{?_isa} = %{version}-%{release}
Provides: %{name}-openmpi3-devel = %{version}-%{release}

%description openmpi3-devel
HDF5 VOL DAOS devel with OpenMPI 3

%package openmpi3-tests
Summary: HDF5 VOL DAOS tests with openmpi3
Requires: %{name}-openmpi3%{?_isa} = %{version}-%{release}

%description openmpi3-tests
HDF5 VOL DAOS tests with openmpi3
%endif

%if %{with_mpich}
%package mpich
Summary: HDF5 VOL DAOS with MPICH
BuildRequires: hdf5-mpich-devel%{?_isa} >= 1.12.1
Provides: %{name}-mpich2 = %{version}-%{release}

%description mpich
HDF5 VOL DAOS with MPICH

%package mpich-devel
Summary: HDF5 VOL DAOS devel with MPICH
Requires: hdf5-mpich-devel%{?_isa}
Requires: %{name}-mpich%{?_isa} = %{version}-%{release}
Provides: %{name}-mpich2-devel = %{version}-%{release}

%description mpich-devel
HDF5 VOL DAOS devel with MPICH

%package mpich-tests
Summary: HDF5 VOL DAOS tests with mpich
Requires: %{name}-mpich%{?_isa} = %{version}-%{release}

%description mpich-tests
HDF5 VOL DAOS tests with mpich

%endif

%if (0%{?suse_version} > 0)
%global __debug_package 1
%global _debuginfo_subpackages 1
%debug_package
%endif

%prep
%setup -n vol-daos-%{vol_tag}
%setup -T -D -b 1 -n vol-daos-%{vol_tag}

cd ../vol-tests-%{vol_test_tag}/
cd ../vol-daos-%{vol_tag}
mv ../vol-tests-%{vol_test_tag}/* test/vol/

%build
for mpi in %{?mpi_list}; do
  mkdir $mpi
  pushd $mpi
  %module_load $mpi
  %{cmake} -DCMAKE_INSTALL_PREFIX=%{mpi_libdir}/$mpi \
        -DBUILD_TESTING=ON \
        -DHDF5_VOL_TEST_ENABLE_PART=ON \
        -DHDF5_VOL_TEST_ENABLE_PARALLEL=ON \
        -DHDF5_VOL_TEST_ENABLE_ASYNC=ON \
        -DHDF5_VOL_DAOS_USE_SYSTEM_HDF5=OFF \
        -DMPI_C_COMPILER=%{mpi_libdir}/$mpi/bin/mpicc \
        -DCMAKE_SKIP_RPATH:BOOL=ON \
        ..
  %{make_build}
  module purge
  popd
done

%install
for mpi in %{?mpi_list}; do
  %module_load $mpi
  %{make_install} -C $mpi
  module purge
  mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/{$mpi/hdf5_vol_daos-tests,hdf5_vol_daos/$mpi}/
  ln -s ../../$mpi/hdf5_vol_daos-tests ${RPM_BUILD_ROOT}%{_libdir}/hdf5_vol_daos/$mpi/tests
  for x in h5_test_testhdf5 h5vl_test h5_partest_t_bigio h5_partest_testphdf5 \
           h5vl_test_parallel h5_partest_t_shapesame h5daos_test_map \
           h5daos_test_map_parallel h5daos_test_oclass \
           h5daos_test_metadata_parallel; do
    install -m 0755 $mpi/bin/${x} ${RPM_BUILD_ROOT}%{_libdir}/$mpi/hdf5_vol_daos-tests/
  done
  module purge
done

%files
%license COPYING

%if %{with_openmpi}
%files openmpi
%license COPYING
%{mpi_libdir}/openmpi/lib/libhdf5_vol_daos.so.*
%{mpi_libdir}/openmpi/share

%files openmpi-devel
%license COPYING
%{mpi_libdir}/openmpi/lib/libhdf5_vol_daos.so
%{mpi_libdir}/openmpi/lib/pkgconfig/
%{mpi_libdir}/openmpi/include/*.h

%files openmpi-tests
%license COPYING
%{_libdir}/openmpi/hdf5_vol_daos-tests
%{_libdir}/hdf5_vol_daos/openmpi/tests
%endif

%if %{with_openmpi3}
%files openmpi3
%license COPYING
%{mpi_libdir}/openmpi3/lib/libhdf5_vol_daos.so.*
%{mpi_libdir}/openmpi3/share

%files openmpi3-devel
%license COPYING
%{mpi_libdir}/openmpi3/lib/libhdf5_vol_daos.so
%{mpi_libdir}/openmpi3/lib/pkgconfig/
%{mpi_libdir}/openmpi3/include/*.h

%files openmpi3-tests
%license COPYING
%{_libdir}/openmpi3/hdf5_vol_daos-tests
%{_libdir}/hdf5_vol_daos/openmpi3/tests
%endif

%if %{with_mpich}
%files mpich
%license COPYING
%{mpi_libdir}/mpich/lib/libhdf5_vol_daos.so.*
%{mpi_libdir}/mpich/share


%files mpich-devel
%license COPYING
%{mpi_libdir}/mpich/lib/libhdf5_vol_daos.so
%{mpi_libdir}/mpich/lib/pkgconfig/
%{mpi_libdir}/mpich/include/*.h

%files mpich-tests
%license COPYING
%{_libdir}/mpich/hdf5_vol_daos-tests
%{_libdir}/hdf5_vol_daos/mpich/tests
%endif

%changelog
* Fri Jan 7 2022 Mohamad Chaarawi <mohamad.chaarawi@intel.com> 1.1.0~rc4-1
- Update to rc4

* Fri Dec 17 2021 Phillip Henderson <phillip.henderson@intel.com> - 1.1.0~rc3-9
- Enable building debuginfo package on SUSE platforms

* Fri Nov 12 2021 Wang Shilong <shilong.wang@intel.com> 1.1.0~rc3-8
- Rebuilt for breaking DAOS API change

* Mon Oct 18 2021 Mohamad Chaarawi <mohamad.chaarawi@intel.com> 1.1.0~rc3-7
- remove BR libfabric-devel

* Thu Oct 7 2021 Mohamad Chaarawi <mohamad.chaarawi@intel.com> 1.1.0~rc3-6
- Bring in patches to add support for labels and fix some bugs in the VOL

* Sun Sep 26 2021 Mohamad Chaarawi <mohamad.chaarawi@intel.com> 1.1.0~rc3-5
- Add patch for vol fix for link creation with order tracking

* Wed Aug 4 2021 Mohamad Chaarawi <mohamad.chaarawi@intel.com> 1.1.0~rc3-4
- Add patch for vol test fixes for DAOS
- add libfabric-devel

* Tue Jun 22 2021 Mohamad Chaarawi <mohamad.chaarawi@intel.com> 1.1.0~rc3-3
- Add patch for uns initializing

* Mon May 17 2021 Brian J. Murrell <brian.murrell@intel.com> - 1.1.0~rc3-2
- Package for openmpi on EL8
- Move tests under %%_libdir/$mpi to keep the dependency generator happy
  - But keep backward compatible paths

* Wed Apr 07 2021 David Maldonado Moreno <david.maldonado.moreno@intel.com> - 1.1.0~rc3-1
- Add 34db47e patch that removes the boost dependencies
- Update hdf5-vol v1.1.0rc3 and vol_tests v0.9.2

* Mon Feb 08 2021 Jonathan Martinez Montes <jonathan.martinez.montes@intel.com> - 1.1.0~rc2-2
- Add test h5daos_test_metadata_parallel

* Wed Feb 03 2021 Maureen Jean <maureen.jean@intel.com> - 1.1.0~rc2-1
- Update hdf5-vol v1.1.0rc2 and vol_tests v0.9.1

* Fri Jan 29 2021 Maureen Jean <maureen.jean@intel.com> - 1.1.0~rc1
- Update hdf5-vol v1.1.0rc1 and vol_tests v0.9.0

* Fri Jan 22 2021 Kenneth Cain <kenneth.c.cain@intel.com> - 0.1-5.gfcbdc0b
- restore requires for mpich-devel/tests and openmpi3-devel/tests

* Wed Jan 20 2021 Kenneth Cain <kenneth.c.cain@intel.com> - 0.1-4.gfcbdc0b
- Update hdf5-vol to fcbdc0b, and virtual provides to build with libdaos.so.1

* Fri Nov 20 2020 Maureen Jean <maureen.jean@intel.com> - 0.1-3.gb8e6afb18f
- Update hdf5-vol to gb8e6afb18f and vol-test to gd3f80a57ca

* Mon Oct  5 2020 Brian J. Murrell <brian.murrell@intel.com> - 0.1-2.gb324b90d4
- Tests packages should not require any -devel packages

* Mon Aug  3 2020 Maureen Jean <maureen.jean@intel.com> - 0.1-1.gb324b90d4
- Initial version - vol tests g31660ab1935
