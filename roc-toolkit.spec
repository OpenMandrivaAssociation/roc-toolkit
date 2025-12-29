%global _lto_cflags %{nil}
#define snapshot 20221117
%undefine _debugsource_packages

%define libname %mklibname roc
%define devname %mklibname roc -d

Name:		roc-toolkit
Version:	0.4.0
Release:	%{?snapshot:0.%{snapshot}.}2
Summary:	Real-time audio streaming
License:	MPL-2.0 AND LGPL-2.1-or-later AND CECILL-C
URL:		https://github.com/roc-streaming/roc-toolkit
Source0:	https://github.com/roc-streaming/roc-toolkit/archive/%{?snapshot:refs/heads/master}%{!?snapshot:v%{version}/%{name}-%{version}}.tar.gz
Patch0:		roc-c++unwind.patch
#Patch1:		https://src.fedoraproject.org/fork/wtaymans/rpms/roc-toolkit/raw/d31d30281a036556dae16f72e7b3d641cb1ce2ad/f/pkgdir.patch
Patch2:		https://patch-diff.githubusercontent.com/raw/roc-streaming/roc-toolkit/pull/822.patch

BuildRequires:	pkgconfig(python)
BuildRequires:  scons
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	gengetopt
BuildRequires:	ragel
BuildRequires:	pkgconfig(libuv)
BuildRequires:	pkgconfig(libunwind)
BuildRequires:	pkgconfig(sox)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(speexdsp)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	openfec-devel
#BuildRequires:	pkgconfig(cpputest)
BuildRequires:	doxygen
BuildRequires:	python%{pyver}dist(sphinx)
BuildRequires:	python%{pyver}dist(breathe)

# https://github.com/roc-streaming/roc-toolkit/issues/481
#Patch0:		roc-toolkit-0.1.5-no-explicit-cpp98.patch
 
%description
Roc is a toolkit for real-time audio streaming over the network.

%package -n %{libname}
Summary: Libraries of the ROC audio streaming toolkit
Group: System/Libraries
%rename %{name}

%description -n %{libname}
Libraries of the ROC audio streaming toolkit
 
%package -n %{devname}
Summary: Development libraries for roc-toolkit
Requires: %{libname}%{?_isa} = %{EVRD}
%rename %{name}-devel
 
%description -n %{devname}
The roc-toolkit-devel package contains header files necessary for
developing programs using roc-toolkit.
 
%package utils
Summary: Utilities for roc-toolkit
Requires: %{libname}%{?_isa} = %{EVRD}
 
%description utils
Utilities for roc-toolkit.
 
%prep
%autosetup -p1 -n %{name}-%{?snapshot:master}%{!?snapshot:%{version}}
 
%build
export PYTHONWARNINGS=default
export PYTHONHASHSEED=0
export PYTHONRECURSIONLIMIT=3000
scons \
	--with-openfec-includes=%{_includedir}/openfec \
	--disable-libunwind CC="%{__cc}" CXX="%{__cxx}"

%install
scons install --with-openfec-includes=%{_includedir}/openfec --prefix=%{buildroot}%{_prefix} \
  --libdir=%{buildroot}%{_libdir} CC="%{__cc}" CXX="%{__cxx}"

%files -n %{libname}
%license LICENSE
%doc README.md
%{_libdir}/libroc.so.0*
 
%files -n %{devname}
%{_includedir}/roc
%{_libdir}/libroc.so
%{_libdir}/pkgconfig/roc.pc
 
%files utils
%{_bindir}/roc-copy
%{_bindir}/roc-recv
%{_bindir}/roc-send
%{_mandir}/man1/*.1*
