#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	SVG loading and drawing library
Summary(pl.UTF-8):	Biblioteka do wczytywania i rysowania obrazów SVG
Name:		dax-svg
Version:	0.1.0
%define	snap	20100802
%define	gitref	c8dc7638977f5b09d3d709b4c0119adf892ba10c
Release:	0.%{snap}.1
License:	LGPL v2.1
Group:		Libraries
Source0:	https://github.com/dlespiau/dax-svg/archive/%{gitref}/%{name}-%{snap}.tar.gz
# Source0-md5:	a4484dc120da5babc3bf9e76c2eaf523
Patch0:		%{name}-clutter.patch
Patch1:		%{name}-gjs.patch
Patch2:		%{name}-pc.patch
URL:		https://github.com/dlespiau/dax-svg/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.10
BuildRequires:	clutter-devel >= 1.3.2
BuildRequires:	clutter-gst-devel >= 3.0
BuildRequires:	gjs-devel >= 1.0
BuildRequires:	glib2-devel >= 1:2.22
BuildRequires:	gobject-introspection-devel >= 0.6.14
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	mozjs24-devel
BuildRequires:	mx-devel >= 1.0
BuildRequires:	pkgconfig
Requires:	clutter >= 1.3.2
Requires:	glib2 >= 1:2.22
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SVG loading and drawing library.

%description -l pl.UTF-8
Biblioteka do wczytywania i rysowania obrazów SVG.

%package devel
Summary:	Header files for Dax library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Dax
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	clutter-devel >= 1.3.2
Requires:	clutter-gst-devel >= 3.0
Requires:	gjs-devel >= 1.0
Requires:	glib2-devel >= 1:2.22
Requires:	libxml2-devel >= 2.0
Requires:	mozjs24-devel
Requires:	mx-devel >= 1.0

%description devel
Header files for Dax library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Dax.

%package static
Summary:	Static Dax library
Summary(pl.UTF-8):	Statyczna biblioteka Dax
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Dax library.

%description static -l pl.UTF-8
Statyczna biblioteka Dax.

%prep
%setup -q -n %{name}-%{gitref}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal} -I build/autotools
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dax-viewer
%attr(755,root,root) %{_libdir}/libdax-0.2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdax-0.2.so.0
%attr(755,root,root) %{_libdir}/libdox-0.2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdox-0.2.so.0
%{_libdir}/girepository-1.0/Dax-0.2.typelib
%{_libdir}/girepository-1.0/Dox-0.2.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdax-0.2.so
%attr(755,root,root) %{_libdir}/libdox-0.2.so
%{_includedir}/dax-0.2
%{_includedir}/dox-0.2
%{_datadir}/gir-1.0/Dax-0.2.gir
%{_datadir}/gir-1.0/Dox-0.2.gir
%{_pkgconfigdir}/dax-0.2.pc
%{_pkgconfigdir}/dox-0.2.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libdax-0.2.a
%{_libdir}/libdox-0.2.a
%endif
