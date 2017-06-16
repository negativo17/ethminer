%global commit0 2d692d263f3ba74a3612ad3bbec9e7cfac413a1f
%global date 20170607
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:           ethminer
Version:        1.1.7
Release:        4%{?shortcommit0:.%{date}git%{shortcommit0}}%{?dist}
Summary:        Ethereum miner with CUDA and stratum support
License:        MIT
URL:            https://github.com/genoil/cpp-ethereum

Source0:        %{url}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz

BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  cuda-devel
BuildRequires:  curl-devel
BuildRequires:  miniupnpc-devel
BuildRequires:  pkgconfig(cryptopp)
BuildRequires:  pkgconfig(jsoncpp)
BuildRequires:  pkgconfig(leveldb)
BuildRequires:  pkgconfig(libjsonrpccpp-server)
BuildRequires:  pkgconfig(libmicrohttpd)
BuildRequires:  pkgconfig(ocl-icd)
BuildRequires:  readline-devel

%if 0%{?fedora}
BuildRequires:  compat-gcc-53-c++
%endif

# libethash-cuda.so dlopens libcuda.so.1
Requires:       nvidia-driver-cuda-libs
Requires:       ocl-icd

%description
Formerly known as Genoil's CUDA miner, ethminer-0.9.41-genoil-1.x.x is a fork
of the stock ethminer version 0.9.41. While native CUDA support is its most
significant difference, it has the following additional features:

 * realistic benchmarking against arbitrary epoch/DAG/blocknumber
 * on-GPU DAG generation (no more DAG files on disk)
 * stratum mining without proxy
 * OpenCL devices picking
 * farm failover (getwork + stratum)

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -qn cpp-ethereum-%{commit0}
# Make CUDA support a shared library
sed -i -s 's/STATIC//g' libethash-cuda/CMakeLists.txt

for file in $(find . -name CMakeLists.txt); do
  sed -i 's|^\(install.*LIBRARY DESTINATION\) lib|\1 %{_lib}|' $file; done
  
# Lower required boost version slightly to make it compile with RHEL7
sed -i 's|Boost 1.54.0 REQUIRED|Boost 1.53.0 REQUIRED|' cmake/EthDependencies.cmake

%build
%if 0%{?fedora}
export CC=/usr/bin/gcc53
export CXX=/usr/bin/g++53
%endif
%cmake -DBUNDLE=cudaminer .
%make_build

%install
%make_install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license GPLV3_LICENSE LICENSE
%doc README.md
%{_bindir}/*
%{_libdir}/*

%files devel
%{_includedir}/*

%changelog
* Fri Jun 16 2017 Simone Caronni <negativo17@gmail.com> - 1.1.7-4.20170607git2d692d2
- Rename to ethminer, not to be confused with cpp-ethereum, the official client.

* Fri Jun 16 2017 Simone Caronni <negativo17@gmail.com> - 1.1.7-3.20170607git2d692d2
- Do not attempt to build the gui.

* Fri Jun 16 2017 Simone Caronni <negativo17@gmail.com> - 1.1.7-2.20170607git2d692d2
- Update to latest snapshot, enable CUDA support.
- Rename to cpp-ethereum.

* Sat Mar 25 2017 Samuel Rakitničan <samuel.rakitnican@gmail.com> 1.1.7-1.20170325git0b1da6b
- Initial build
