#define snapshot 20221117
%undefine _debugsource_packages

Name:		roc-toolkit
Version:	0.3.0
Release:	%{?snapshot:0.%{snapshot}.}1
Summary:	Real-time audio streaming
License:	MPL-2.0 AND LGPL-2.1-or-later AND CECILL-C
URL:		https://github.com/roc-streaming/roc-toolkit
Source0:	https://github.com/roc-streaming/roc-toolkit/archive/%{?snapshot:refs/heads/master}%{!?snapshot:v%{version}/%{name}-%{version}}.tar.gz
Patch0:		roc-c++unwind.patch
Patch1:		https://src.fedoraproject.org/fork/wtaymans/rpms/roc-toolkit/raw/d31d30281a036556dae16f72e7b3d641cb1ce2ad/f/pkgdir.patch

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
BuildRequires:	pkgconfig(speexdsp)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	openfec-devel
#BuildRequires:	pkgconfig(cpputest)
BuildRequires:	doxygen
BuildRequires:	python-sphinx
BuildRequires:	python-breathe

# https://github.com/roc-streaming/roc-toolkit/issues/481
#Patch0:		roc-toolkit-0.1.5-no-explicit-cpp98.patch
 
%description
Roc is a toolkit for real-time audio streaming over the network.
 
%package devel
Summary: Development libraries for roc-toolkit
Requires: %{name}%{?_isa} = %{version}-%{release}
 
%description devel
The roc-toolkit-devel package contains header files necessary for
developing programs using roc-toolkit.
 
%package utils
Summary: Utilities for roc-toolkit
Requires: %{name}%{?_isa} = %{version}-%{release}
 
%description utils
Utilities for roc-toolkit.
 
%package doc
Summary: Documentation for roc-toolkit
 
%description doc
Documentation for roc-toolkit.
 
%prep
%autosetup -p1 -n %{name}-%{?snapshot:master}%{!?snapshot:%{version}}
 
%build
scons \
	--with-openfec-includes=%{_includedir}/openfec \
	--disable-libunwind CC=%{__cc} CXX=%{__cxx}

%install
scons install --with-openfec-includes=%{_includedir}/openfec --prefix=%{buildroot}%{_prefix} \
  --libdir=%{buildroot}%{_libdir} CC=%{__cc} CXX=%{__cxx}

%files
%license LICENSE
%doc README.md
%{_libdir}/libroc.so.0*
 
%files devel
%{_includedir}/roc
%{_libdir}/libroc.so
%{_libdir}/pkgconfig/roc.pc
 
%files utils
%{_bindir}/roc-copy
%{_bindir}/roc-recv
%{_bindir}/roc-send
%{_mandir}/man1/*.1*
 
%files doc
