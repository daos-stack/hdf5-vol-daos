%global with_mpich 1
%global with_openmpi3 1

%global daos_major 1

%if %{with_mpich}
%global mpi_list mpich
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
Version: 0.1
Release: 4%{?relval}%{?dist}
Summary: A Multi-purpose, Application-Centric, Scalable I/O Proxy Application

License: GPL
URL: https://portal.hdfgroup.org/display/HDF5/HDF5
Source0: %{source_commit}.tar.gz
Source1: %{test_commit}.tar.gz

BuildRequires: daos-devel%{?_isa}
BuildRequires: gcc, gcc-c++
%if (0%{?suse_version} >= 1500)
BuildRequires: cmake >= 3.1
BuildRequires: lua-lmod
%else
BuildRequires: cmake3 >= 3.1
BuildRequires: Lmod
%endif
BuildRequires: hdf5-devel%{?_isa}
Provides:       %{name}-daos-%{daos_major} = %{version}-%{release}

%description
HDF5 VOL DAOS connector is used to leverage the
capabilities of the DAOS object storage system
within an HDF5 application.  It translates HDF5 VOL
storage related calls into native daos storage operations

%if %{with_mpich}
%package mpich
Summary: HDF5 VOL DAOS with MPICH
BuildRequires: hdf5-mpich-devel%{?_isa}
Provides: %{name}-mpich2 = %{version}-%{release}
Provides: %{name}-mpich2-daos-%{daos_major} = %{version}-%{release}

%description mpich
HDF5 VOL DAOS with MPICH

%package mpich-devel
Summary: HDF5 VOL DAOS devel with MPICH
BuildRequires: hdf5-mpich-devel%{?_isa}
Requires: hdf5-mpich-devel%{?_isa}
Requires: %{name}-mpich2
Provides: %{name}-mpich2-devel = %{version}-%{release}

%description mpich-devel
HDF5 VOL DAOS devel with MPICH

%package mpich-tests
Summary: HDF5 VOL DAOS tests with mpich
BuildRequires: hdf5-mpich-devel%{?_isa}
Requires: %{name}-mpich2
Provides: %{name}-mpich2-tests-daos-%{daos_major} = %{version}-%{release}

%description mpich-tests
HDF5 VOL DAOS tests with mpich

%endif

%if %{with_openmpi3}
%package openmpi3
Summary: HDF5 VOL DAOS with OpenMPI 3
BuildRequires: hdf5-openmpi3-devel%{?_isa}
Provides: %{name}-openmpi3 = %{version}-%{release}
Provides: %{name}-openmpi3-daos-%{daos_major} = %{version}-%{release}

%description openmpi3
HDF5 VOL DAOS with OpenMPI 3

%package openmpi3-devel
Summary: HDF5 VOL DAOS devel with OpenMPI 3
BuildRequires: hdf5-openmpi3-devel%{?_isa}
Requires: hdf5-openmpi3-devel%{?_isa}
Requires: %{name}-openmpi3
Provides: %{name}-openmpi3-devel = %{version}-%{release}

%description openmpi3-devel
HDF5 VOL DAOS devel with OpenMPI 3

%package openmpi3-tests
Summary: HDF5 VOL DAOS tests with openmpi3
BuildRequires: hdf5-openmpi3-devel%{?_isa}
Requires: %{name}-openmpi3
Provides: %{name}-openmpi3-tests-daos-%{daos_major} = %{version}-%{release}

%description openmpi3-tests
HDF5 VOL DAOS tests with openmpi3
%endif

%prep
%setup -n vol-daos-%{source_commit}
%setup -T -D -b 1 -n vol-daos-%{source_commit}
mv ../vol-tests-%{test_commit}/* test/vol/

%build
for mpi in %{?mpi_list}
do
  mkdir $mpi
  pushd $mpi
  %module_load $mpi
  %{cmake} -DCMAKE_INSTALL_PREFIX=%{mpi_libdir}/$mpi \
        -DBUILD_TESTING=ON \
        -DHDF5_VOL_TEST_ENABLE_PART=ON \
        -DHDF5_VOL_TEST_ENABLE_PARALLEL=ON \
        -DHDF5_VOL_DAOS_USE_SYSTEM_HDF5=OFF \
        -DMPI_C_COMPILER=%{mpi_libdir}/$mpi/bin/mpicc \
        -DCMAKE_SKIP_RPATH:BOOL=ON \
        ..
  %{make_build}
  module purge
  popd
done

%install
for mpi in %{?mpi_list}
do
  %module_load $mpi
  %{make_install} -C $mpi
  module purge
  mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/hdf5_vol_daos/$mpi/tests/
  for x in h5_test_testhdf5 h5vl_test h5_partest_t_bigio h5_partest_testphdf5 \
           h5vl_test_parallel h5_partest_t_shapesame h5daos_test_map \
           h5daos_test_map_parallel h5daos_test_oclass
  do
    install -m 0755 $mpi/bin/${x} ${RPM_BUILD_ROOT}%{_libdir}/hdf5_vol_daos/$mpi/tests/
  done
done

%files
%license COPYING

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
%{_libdir}/hdf5_vol_daos/mpich/tests
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
%{_libdir}/hdf5_vol_daos/openmpi3/tests
%endif

%changelog
* Mon Dec 14 2020 Kenneth Cain <kenneth.c.cain@intel.com> - 0.1-4.gfcbdc0b32d
- Update hdf5-vol to gfcbdc0b32d and virtual provides to build with libdaos.so.1

* Fri Nov 20 2020 Maureen Jean <maureen.jean@intel.com> - 0.1-3.gb8e6afb18f
- Update hdf5-vol to gb8e6afb18f and vol-test to gd3f80a57ca

* Mon Oct  5 2020 Brian J. Murrell <brian.murrell@intel.com> - 0.1-2.gb324b90d4
- Tests packages should not require any -devel packages

* Mon Aug  3 2020 Maureen Jean <maureen.jean@intel.com> - 0.1-1.gb324b90d4
- Initial version - vol tests g31660ab1935
