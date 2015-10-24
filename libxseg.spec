#
# Conditional build:
%bcond_without	doc		# Sphinx documentation
#
Summary:	The low-level communication library of Archipelago
Summary(pl.UTF-8):	Niskopoziomowa biblioteka komunikacji dla Archipelago
Name:		libxseg
Version:	0.4.1
Release:	1
License:	GPL v3+
Group:		Libraries
Source0:	https://github.com/grnet/libxseg/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	75c4afa0ce0065ff594b48cdb7901baa
Patch0:		%{name}-archs.patch
Patch1:		%{name}-libdir.patch
URL:		https://github.com/grnet/libxseg
BuildRequires:	cmake >= 2.8
# h2xml, xml2py
BuildRequires:	python-ctypeslib
BuildRequires:	python-devel
BuildRequires:	python-setuptools
%if %{with doc}
BuildRequires:	sphinx-pdg
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libxseg is a shared memory communication library. It is designed to
provide fast inter-process communication between distinct processes.
It is based on shared memory areas (segments) that each process (peer)
can map on its own address space. It lays down endpoints (ports),
messages (requests), and buffers over the shared segment. It also
specifies an API to interact with the segment and pass messages
between peers.

Its primary use is to support Archipelago's modular architecture and
provide low-latency message passing between different Archipelago
peers.

%description -l pl.UTF-8
Libxseg to biblioteka komunikacji przez pamięć współdzieloną. Została
zaprojektowana w celu szybkiej komunikacji międzyprocesowej między
osobnymi procesami. Jest oparta na obszarach (segmentach) pamięci
współdzielonej, które każdy proces (strona komunikacji) może
odwzorować we własnej przestrzeni adresowej. Wewnątrz tych segmentów
umieszcza zakończenia (porty), komunikaty (żądania) oraz bufory.
Określa także API do współpracy z segmentami oraz przesyłaniem
komunikatów między stronami.

Głównym zastosowaniem jest wspardzie architektury modularnej
Archipelago oraz zapewnienie szybkiego przekazywania komunikatów
między różnymi stronami Archipelago.

%package devel
Summary:	Header files for xseg library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki xseg
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for xseg library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki xseg.

%package doc
Summary:	xseg documentation
Summary(pl.UTF-8):	Dokumentacja biblioteki xseg
Group:		Documentation

%description doc
Documentation for xseg library.

%description doc -l pl.UTF-8
Dokumentacja biblioteki xseg.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
install -d build
cd build
%cmake ..
%{__make}
cd ..

%if %{with doc}
%{__make} -C docs html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYRIGHT Changelog README.md
%attr(755,root,root) %{_bindir}/xseg
%attr(755,root,root) %{_libdir}/libxseg.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libxseg.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxseg.so
%{_includedir}/xseg

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
