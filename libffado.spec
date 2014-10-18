%define		svnrev	%{nil}

# svn checkout http://subversion.ffado.org/ffado/branches/libffado-2.0 libffado-2.0-svn
# mv libffado-2.0-svn libffado-2.0.1
# tar -cf - libffado-2.0.1 | xz -9e -c > libffado-2.0.1.tar.xz
# Source0:	%{name}-%{version}-%{svnrev}.tar.xz

%bcond_without	jack	# for bootstrap

Summary:	Free FireWire Audio Drivers
Name:		libffado
Version:	2.2.1
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://www.ffado.org/files/%{name}-%{version}.tgz
# Source0-md5:	e113d828835051f835fb4a329cb0cbd4
URL:		http://www.ffado.org/
BuildRequires:	dbus-c++-devel
BuildRequires:	expat-devel
BuildRequires:	glibmm-devel
BuildRequires:	libavc1394-devel
BuildRequires:	libconfig-c++-devel
BuildRequires:	libiec61883-devel
BuildRequires:	libraw1394-devel
BuildRequires:	libxml++-devel
BuildRequires:	libxml2-devel
BuildRequires:	pkg-config
BuildRequires:	python-PyQt-QtDBus
BuildRequires:	python-PyQt-devel
BuildRequires:	scons
%{?with_jack:BuildRequires:	jack-audio-connection-kit-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Free FireWire Audio Drivers.

%package utils
Summary:	FFADO utilities
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	dbus
Requires:	python-PyQt
Requires:	python-PyQt-QtDBus

%description utils
FFADO utilities.

%package devel
Summary:	Header files for ffado library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This is the package containing the header files for ffado library.

%prep
%setup -q

%build
export LDFLAGS="%{rpmldflags} -fPIC"

%{__sed} -i -e 's|-O2|%{rpmcflags}|g' SConstruct
%{__sed} -i -e 's|-$REVISION||' version.h.in

%{__scons} \
	BUILD_TESTS=0			\
	DEBUG=0				\
	DESTDIR=$RPM_BUILD_ROOT		\
	DIST_TARGET="%{_target_cpu}"	\
	LIBDIR=%{_libdir}		\
	MANDIR=%{_mandir}		\
	PREFIX=%{_prefix}		\
	UDEVDIR=/usr/lib/udev/rules.d	\
	WILL_DEAL_WITH_XDG_MYSELF="True"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}

%{__scons} install		\
	DEBUG=0			\
	DESTDIR=$RPM_BUILD_ROOT	\
	MANDIR=%{_mandir}	\
	PREFIX=%{_prefix}	\
	WILL_DEAL_WITH_XDG_MYSELF="True"

%{__sed} -i 's/\ #.*$//g' \
	$RPM_BUILD_ROOT%{_prefix}/lib/udev/rules.d/60-ffado.rules

%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean

install support/xdg/hi64-apps-ffado.png \
	$RPM_BUILD_ROOT%{_pixmapsdir}/ffado.png

cat > $RPM_BUILD_ROOT%{_desktopdir}/ffado-mixer.desktop <<EOF
[Desktop Entry]
Type=Application
Exec=ffado-mixer
Icon=ffado
Terminal=false
Name=FFADO mixer
Comment=Mixer for firewire based (semi-) professional audio cards
Categories=Qt;Audio;AudioVideo;Mixer;Settings;HardwareSettings;
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libffado.so.?
%attr(755,root,root) %{_libdir}/libffado.so.*.*.*

%files utils
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/ffado-bridgeco-downloader
%attr(755,root,root) %{_bindir}/ffado-dbus-server
%attr(755,root,root) %{_bindir}/ffado-diag
%attr(755,root,root) %{_bindir}/ffado-dice-firmware
%attr(755,root,root) %{_bindir}/ffado-fireworks-downloader
%attr(755,root,root) %{_bindir}/ffado-mixer
%attr(755,root,root) %{_bindir}/ffado-set-nickname

%{_datadir}/libffado/configuration
%{_datadir}/dbus-1/services/org.ffado.Control.service
%{_prefix}/lib/udev/rules.d/60-ffado.rules

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/icons
%{_datadir}/%{name}/python
%{_datadir}/%{name}/*.xml
%{py_sitescriptdir}/ffado

%{_desktopdir}/ffado-mixer.desktop
%{_pixmapsdir}/ffado.png
%{_mandir}/man1/ffado-*.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libffado.so
%{_includedir}/%{name}
%{_pkgconfigdir}/%{name}.pc

