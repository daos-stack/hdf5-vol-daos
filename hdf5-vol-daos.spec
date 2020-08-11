%global with_mpich 1
%global with_openmpi3 1

%if %{with_mpich}
%global mpi_list mpich
%endif
%if %{with_openmpi3}
%global mpi_list %{?mpi_list} openmpi3
%endif

%if (0%{?suse_version} >= 1500)
%global module_load() if [ "%{1}" == "openmpi3" ]; then module load gnu-openmpi; else module load gnu-%{1}; fi
%else
%global module_load() module load mpi/%{1}-%{_arch}
%endif

Name:    hdf5-vol-daos
Version: 1.0
Release: 1.gb324b90d455%{?dist}
Summary: A Multi-purpose, Application-Centric, Scalable I/O Proxy Application

License: GPL
URL: https://portal.hdfgroup.org/display/HDF5/HDF5
Source0: https://bitbucket.hdfgroup.org/rest/archive/latest/projects/HDF5VOL/repos/daos-vol/archive?format=tgz
Source1: https://bitbucket.hdfgroup.org/rest/archive/latest/projects/HDF5VOL/repos/vol-tests/archive?format=tgz

BuildRequires: gcc, gcc-c++
BuildRequires: cmake
BuildRequires: hdf5-devel%{?_isa}
%if (0%{?suse_version} >= 1500)
BuildRequires: ed
BuildRequires: Modules
%else
BuildRequires: environment-modules
%endif
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
BuildRequires: mpich-devel%{?_isa}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description mpich
HDF5 VOL DAOS with MPICH

%package mpich-devel
Summary: HDF5 VOL DAOS devel with MPICH
BuildRequires: hdf5-mpich-devel%{?_isa}
BuildRequires: mpich-devel%{?_isa}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description mpich-devel
HDF5 VOL DAOS devel with MPICH

%package mpich-tests
Summary: HDF5 VOL DAOS tests with mpich
BuildRequires: hdf5-mpich-devel%{?_isa}
BuildRequires: mpich-devel%{?_isa}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description mpich-tests
HDF5 VOL DAOS tests with mpich

%endif

%if %{with_openmpi3}
%package openmpi3
Summary: HDF5 VOL DAOS with OpenMPI 3
BuildRequires: hdf5-openmpi3-devel%{?_isa}
BuildRequires: openmpi3-devel%{?_isa}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description openmpi3
HDF5 VOL DAOS with OpenMPI 3

%package openmpi3-devel
Summary: HDF5 VOL DAOS devel with OpenMPI 3
BuildRequires: hdf5-openmpi3-devel%{?_isa}
BuildRequires: openmpi3-devel%{?_isa}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description openmpi3-devel
HDF5 VOL DAOS devel with OpenMPI 3

%package openmpi3-tests
Summary: HDF5 VOL DAOS tests with openmpi3
BuildRequires: hdf5-openmpi3-devel%{?_isa}
BuildRequires: openmpi3-devel%{?_isa}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description openmpi3-tests
HDF5 VOL DAOS tests with openmpi3
%endif

%prep
%setup -c
cd test/vol
/usr/bin/unzip %SOURCE1

%build
for mpi in %{?mpi_list}
do
  mkdir $mpi
  pushd $mpi
  %module_load $mpi
  cmake -DCMAKE_INSTALL_PREFIX=%{_libdir}/$mpi \
        -DBUILD_TESTING=ON \
        -DHDF5_VOL_TEST_ENABLE_PART=ON \
        -DHDF5_VOL_TEST_ENABLE_PARALLEL=ON \
        -DHDF5_VOL_DAOS_USE_SYSTEM_HDF5=OFF \
        -DDAOS_UNIFIED_NAMESPACE_LIBRARY=%{_libdir}/libduns.so \
        -DMPI_C_COMPILER=%{_libdir}/$mpi/bin/mpicc \
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
           h5vl_test_parallel h5_partest_t_shapesame
  do
    install -m 0755 $mpi/bin/${x} ${RPM_BUILD_ROOT}%{_libdir}/hdf5_vol_daos/$mpi/tests/
  done
done

%files
%license COPYING

%if %{with_mpich}
%files mpich
%license COPYING
%{_libdir}/mpich/lib/libhdf5_vol_daos.so.*
%{_libdir}/mpich/share

%files mpich-devel
%license COPYING
%{_libdir}/mpich/lib/libhdf5_vol_daos.so
%{_libdir}/mpich/lib/pkgconfig/
%{_libdir}/mpich/include/*.h

%files mpich-tests
%license COPYING
%{_libdir}/hdf5_vol_daos/mpich/tests
%endif

%if %{with_openmpi3}
%files openmpi3
%license COPYING
%{_libdir}/openmpi3/lib/libhdf5_vol_daos.so.*
%{_libdir}/openmpi3/share

%files openmpi3-devel
%license COPYING
%{_libdir}/openmpi3/lib/libhdf5_vol_daos.so
%{_libdir}/openmpi3/lib/pkgconfig/
%{_libdir}/openmpi3/include/*.h

%files openmpi3-tests
%license COPYING
%{_libdir}/hdf5_vol_daos/openmpi3/tests
%endif

%changelog
* Mon Aug 3 2020 Maureen Jean <maureen.jean@intel.com> - 1.0-1.gb324b90d455
- Initial version - vol tests g31660ab1935