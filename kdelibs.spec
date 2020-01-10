%define attica_ver 0.4.2
%define dbusmenu_qt_ver 0.9.0
%define phonon_ver 4.6.0
%define qt4_ver 4.8.1
%define shared_desktop_ontologies_ver 0.10.0
%define soprano_ver 2.8.0
%define strigi_ver 0.7.0
%define apidocs 1
%if 0%{?epel} || 0%{?fedora}
%define webkit 1
%endif
%if 0%{?fedora}
%define herqq 1
%endif
# to build/include QCH apidocs or not (currently broken)
#define apidocs_qch 1
%if 0%{?rhel} > 6 || 0%{?fedora} > 17
%define udisks udisks2
%define udisks2 1
%else
%define udisks udisks
%endif
%if 0%{?rhel} == 6
%define hal 1
%else
%define upower 1
%endif

%global phonon_version %(pkg-config --modversion phonon 2>/dev/null || echo %{phonon_ver})
%global shared_desktop_ontologies_version %(pkg-config --modversion shared-desktop-ontologies 2>/dev/null || echo %{shared_desktop_ontologies_ver})
%global soprano_version %(pkg-config --modversion soprano 2>/dev/null || echo %{soprano_ver})
%global strigi_version %(pkg-config --modversion libstreams 2>/dev/null || echo %{strigi_ver})
%global dbusmenu_qt_version %(pkg-config --modversion dbusmenu-qt 2>/dev/null || echo %{dbusmenu_qt_ver})
%global rpm_macros_dir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

# trim changelog included in binary rpms
%global _changelog_trimtime %(date +%s -d "1 year ago")

Summary: KDE Libraries
# shipped with kde applications, version...
%global apps_version 15.04.1
Version: 4.14.8
Release: 6%{?dist}

Name: kdelibs
Epoch: 6
Obsoletes: kdelibs4 < %{version}-%{release}
Provides:  kdelibs4 = %{version}-%{release}
%{?_isa:Provides: kdelibs4%{?_isa} = %{version}-%{release}}

# http://techbase.kde.org/Policies/Licensing_Policy
License: LGPLv2+
URL:     http://www.kde.org/
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/applications/%{apps_version}/src/kdelibs-%{version}.tar.xz

Source1: macros.kdelibs4

Source10: SOLID_HAL_LEGACY.sh

BuildRequires: kde4-macros(api) >= 2
BuildRequires: kde-filesystem >= 4-23
# for the RPM dependency generators
BuildRequires: kde-settings
BuildRequires: docbook-dtds docbook-style-xsl
Requires: ca-certificates
Requires: dbusmenu-qt%{?_isa} >= %{dbusmenu_qt_version}
Requires: docbook-dtds docbook-style-xsl
Requires: hicolor-icon-theme
Requires: kde-filesystem >= 4-23
Requires: kde-settings
%{?_kde4_macros_api:Requires: kde4-macros(api) = %{_kde4_macros_api} }
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires: hunspell
Requires: media-player-info
# beware of possible bootstrapping problems
# moved back to kde-runtime
#Requires: oxygen-icon-theme >= %{version}
Requires: phonon%{?_isa} >= %{phonon_version}
Requires: shared-mime-info
Requires: strigi-libs%{?_isa} >= %{strigi_version}
%if ! 0%{?nepomuk}
Requires: shared-desktop-ontologies >= %{shared_desktop_ontologies_version}
Requires: soprano%{?_isa} >= %{soprano_version}
%endif


# make kdelibs-devel parallel-installable with kdelibs3-devel
Patch0: kdelibs-4.9.95-parallel_devel.patch

# fix http://bugs.kde.org/149705
Patch2: kdelibs-4.10.0-kde149705.patch

# install all .css files and Doxyfile.global in kdelibs-common to build
# kdepimlibs-apidocs against
Patch8: kdelibs-4.3.90-install_all_css.patch

# add Fedora/V-R to KHTML UA string
Patch9: kdelibs-4.10.0-branding.patch

# adds the Administration menu from redhat-menus which equals System + Settings
# This prevents the stuff getting listed twice, under both System and Settings.
Patch12: kdelibs-4.10.0-xdg-menu.patch

# patch KStandardDirs to use %{_libexecdir}/kde4 instead of %{_libdir}/kde4/libexec
Patch14: kdelibs-4.11.3-libexecdir.patch

# kstandarddirs changes: search /etc/kde, find %{_kde4_libexecdir}
Patch18: kdelibs-4.11.97-kstandarddirs.patch

# set build type
Patch20: kdelibs-4.10.0-cmake.patch

# die rpath die, since we're using standard paths, we can avoid
# this extra hassle (even though cmake is *supposed* to not add standard
# paths (like /usr/lib64) already! With this, we can drop
# -DCMAKE_SKIP_RPATH:BOOL=ON (finally)
Patch27: kdelibs-4.10.0-no_rpath.patch

## libplasma PackageKit integration
# Trigger installation of missing components when installing a package.
# https://git.reviewboard.kde.org/r/102291/
Patch41: 0002-Trigger-installation-of-missing-components-when-inst.patch

# Implement automatic scanning of source code for required data engines.
# https://git.reviewboard.kde.org/r/102350/
Patch42: 0003-Implement-automatic-scanning-of-source-code-for-requ.patch

# limit solid qDebug spam
# http://bugzilla.redhat.com/882731
# TODO: could make uptreamable and conditional only on Release-type builds
Patch49: kdelibs-solid_qt_no_debug_output.patch

## upstreamable
# knewstuff2 variant of:
# https://git.reviewboard.kde.org/r/102439/
Patch50: kdelibs-4.7.0-knewstuff2_gpg2.patch

# Toggle solid upnp support at runtime via env var SOLID_UPNP=1 (disabled by default)
Patch52: kdelibs-4.10.0-SOLID_UPNP.patch

# add s390/s390x support in kjs
Patch53: kdelibs-4.7.2-kjs-s390.patch

# return valid locale (RFC 1766)
Patch54: kdelibs-4.8.4-kjs-locale.patch

# borrow from  opensuse
# https://build-test.opensuse.org/package/view_file/home:coolo:test/kdelibs4/0001-Drop-Nepomuk-from-KParts-LINK_INTERFACE_LIBRARIES.patch
Patch55: Drop-Nepomuk-from-KParts-LINK_INTERFACE_LIBRARIES.patch

# candidate fix for: kde deamon crash on wakeup
# https://bugs.kde.org/show_bug.cgi?id=288410
Patch56: kdelibs-kdebug288410.patch

# make filter working, TODO: upstream?  -- rex
Patch59: kdelibs-4.9.3-kcm_ssl.patch

# disable dot to reduce apidoc size
Patch61: kdelibs-4.12.90-dot.patch

# make kpac dhcp helper full relro
Patch62: kdelibs-4.10.5-kpac-relro.patch

# make cmake generated files multilib friendly
Patch63: kdelibs-4.10.5-cmake-multilib.patch

# disable strict aliasing for type punned sources
Patch64: kdelibs-4.10.5-type-punning.patch

# workaround for bz#969524 on arm
Patch65: kdelibs-4.11.3-arm.patch

# set QT_NO_GLIB in klauncher_main.cpp as a possible fix/workaround for #983110
Patch66: kdelibs-4.11.3-klauncher-no-glib.patch

# opening a terminal in Konqueror / Dolphin does not inherit environment variables
Patch67: kdelibs-4.13.2-invokeTerminal.patch

## upstream
# 4.14 branch

# revert these commits for
#https://bugs.kde.org/315578
# for now, causes regression,
#https://bugs.kde.org/317138
Patch090: return-not-break.-copy-paste-error.patch
Patch091: coding-style-fixes.patch
Patch092: return-application-icons-properly.patch

# revert disabling of packagekit
Patch093: turn-the-packagekit-support-feature-off-by-default.patch

## security fix
# Bug 1452068 - CVE-2017-8422 kdelibs: kauth: service invoking dbus is not properly checked and allows local privilege escalation
Patch80: kdelibs-kauth-CVE-2017-8422.patch

# rhel patches
Patch100: solid-upower-0.99.patch
Patch101: kdelibs-4.3.4-bz#587016.patch

# disable webkit
Patch300: kdelibs-4.10.0-webkit.patch

# set abrt default
Patch301: kdelibs-4.x-abrt.patch

# kmailservice/ktelnetservice moved here
Conflicts: kdelibs3 < 3.5.10-42

BuildRequires: qt4-devel >= %{qt4_ver}
%if 0%{?webkit}
BuildRequires: pkgconfig(QtWebKit)
%endif
%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}
Requires: xdg-utils
Requires: redhat-menus
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildRequires: automoc4 >= 0.9.88
BuildRequires: bison flex
BuildRequires: bzip2-devel
BuildRequires: cmake >= 2.8.9
BuildRequires: cups-devel cups
BuildRequires: gettext-devel
BuildRequires: giflib-devel
BuildRequires: grantlee-devel
%if 0%{?herqq}
BuildRequires: herqq-devel
%endif
BuildRequires: krb5-devel
BuildRequires: libacl-devel libattr-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: libutempter-devel
# strictly only a runtime dependency, but makes cmake happier at buildtime too -- rex
BuildRequires: media-player-info
BuildRequires: pkgconfig(alsa)
BuildRequires: pkgconfig(avahi-core)
BuildRequires: pkgconfig(dbusmenu-qt)
BuildRequires: pkgconfig(enchant)
BuildRequires: pkgconfig(gamin)
BuildRequires: pkgconfig(jasper)
BuildRequires: pkgconfig(libattica) >= %{attica_ver}
BuildRequires: pkgconfig(liblzma)
BuildRequires: pkgconfig(libpcre)
BuildRequires: pkgconfig(libstreams) >= %{strigi_ver}
BuildRequires: pkgconfig(libudev)
BuildRequires: pkgconfig(libxslt) pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(OpenEXR)
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(phonon) >= %{phonon_ver}
BuildRequires: pkgconfig(polkit-qt-1)
BuildRequires: pkgconfig(qca2)
BuildRequires: pkgconfig(shared-desktop-ontologies) >= %{shared_desktop_ontologies_ver}
BuildRequires: pkgconfig(shared-mime-info)
BuildRequires: pkgconfig(soprano) >= %{soprano_ver}
BuildRequires: pkgconfig(zlib)
# extra X deps (seemingly needed and/or checked-for by most kde4 buildscripts)
%define x_deps pkgconfig(sm) pkgconfig(xcomposite) pkgconfig(xdamage) pkgconfig(xkbfile) pkgconfig(xpm) pkgconfig(xproto) pkgconfig(xscrnsaver) pkgconfig(xtst) pkgconfig(xv) pkgconfig(xxf86misc)
%{?x_deps:BuildRequires: %{x_deps}}

%{?udisks:Requires: %{udisks}}
%{?upower:Requires: upower}
%if 0%{?hal:1}
BuildRequires: hal-devel
Requires: hal-storage-addon
%endif

%if 0%{?apidocs}
BuildRequires: docbook-dtds
BuildRequires: doxygen
BuildRequires: graphviz
# should probably do something about removing this one, it's quite huge'ish -- Rex
BuildRequires: qt4-doc
%endif

%if 0%{?tests}
%global _kde4_build_tests -DKDE4_BUILD_TESTS:BOOL=ON
# %%%check
BuildRequires: dbus-x11 xorg-x11-server-Xvfb
%endif

Provides: katepart = %{version}-%{release}
Provides: katepart%{?_isa} = %{version}-%{release}
Provides: kross(javascript) = %{version}-%{release}
Provides: kross(qtscript) = %{version}-%{release}

%if 0%{?rhel} && 0%{?rhel} < 8
Provides: kdelibs-experimental = %{version}-%{release}
Obsoletes: kdelibs-experimental < 4.3.75
%endif

%description
Libraries for KDE 4.

%package common
Summary: Common files for KDE 3 and KDE 4 libraries
# some files moved kdebase-runtime -> here
Conflicts: kdebase-runtime < 4.5.80
%description common
This package includes the common files for the KDE 3 and KDE 4 libraries.

%package devel
Summary: Header files for compiling KDE 4 applications
Provides: plasma-devel = %{version}-%{release}
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-ktexteditor%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes: kdelibs4-devel < %{version}-%{release}
Provides:  kdelibs4-devel = %{version}-%{release}
Provides:  kdelibs4-devel%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} < 8
Conflicts: kdebase-workspace-devel < 4.3.80
Obsoletes: kdelibs-experimental-devel < 4.3.75
Provides:  kdelibs-experimental-devel = %{version}-%{release}
%endif
Requires: automoc4 >= 0.9.88
Requires: cmake >= 2.8.9
Requires: pkgconfig(libattica) >= %{attica_ver}
Requires: pkgconfig(openssl)
Requires: pkgconfig(phonon)
%if ! 0%{?nepomuk}
# considered part of nepomuk-devel
Provides: nepomuk-devel = %{version}-%{release}
Requires: pkgconfig(shared-desktop-ontologies) pkgconfig(soprano)
Requires: qt4-devel
%if 0%{?webkit}
Requires: pkgconfig(QtWebKit)
%endif
%endif
%{?x_deps:Requires: %{x_deps}}

%description devel
This package includes the header files you will need to compile
applications for KDE 4.

## TODO: split out ktexteditor-devel bits too? -- rex
%package ktexteditor
Summary: KDE4 Text Editor component library
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%if ! 0%{?bootstrap}
Requires: kate-part%{?_isa}
%endif
%description ktexteditor
%{summary}

%package webkit
Summary: KDE WebKit support library
# upgrade path, when -webkit subpkg landed
Obsoletes: kdelibs < 6:4.13.2-6
Provides:  kdelibs4-webkit = %{version}-%{release}
%{?_isa:Provides: kdelibs4-webkit%{?_isa} = %{version}-%{release}}
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%description webkit
%{summary}.

%package webkit-devel
Summary: Development files for KDE WebKit support library
# upgrade path, when -webkit subpkg landed
Obsoletes: kdelibs-devel < 6:4.13.2-6
Provides:  kdelibs4-webkit-devel = %{version}-%{release}
%{?_isa:Provides: kdelibs4-webkit-devel%{?_isa} = %{version}-%{release}}
Requires: %{name}-webkit%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-devel%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: pkgconfig(QtWebKit)
%description webkit-devel
%{summary}.

%package apidocs
Summary: KDE 4 API documentation
Requires: kde-filesystem
Provides: kdelibs4-apidocs = %{version}-%{release}
BuildArch: noarch

%description apidocs
This package includes the KDE 4 API documentation in HTML
format for easy browsing.

%package apidocs-qch
Summary: KDE 4 API documentation for Qt Assistant
# Directory ownership (%{_qt4_docdir}/qch)
Requires: qt4
Provides: kdelibs4-apidocs-qch = %{version}-%{release}
BuildArch: noarch

%description apidocs-qch
This package includes the KDE 4 API documentation in Qt Assistant QCH
format for use with the Qt 4 Assistant or KDevelop 4.


%prep
%setup -q -n kdelibs-%{version}

%patch0 -p1 -b .parallel_devel
%patch2 -p1 -b .kde149705
%patch8 -p1 -b .install_all_css
%patch9 -p1 -b .branding
# add release version as part of branding (suggested by cailon)
sed -i -e "s|@@VERSION_RELEASE@@|%{version}-%{release}|" kio/kio/kprotocolmanager.cpp
%patch12 -p1 -b .Administration-menu
%patch14 -p1 -b .libexecdir
%patch18 -p1 -b .kstandarddirs
%patch20 -p1 -b .xxcmake
%patch27 -p1 -b .no_rpath

# libplasma PackageKit integration
%patch41 -p1 -b .libplasma-pk-0002
%patch42 -p1 -b .libplasma-pk-0003

%if "%{?udisks}" == "udisks2"
%patch49 -p1 -b .solid_qt_no_debug_output
%endif

# upstreamable patches
%patch50 -p1 -b .knewstuff2_gpg2
%patch52 -p1 -b .SOLID_UPNP
%patch53 -p1 -b .kjs-s390
%patch54 -p1 -b .kjs-locale
%patch55 -p1 -b .Drop-Nepomuk-from-KParts-LINK_INTERFACE_LIBRARIES
%patch56 -p1 -b .kdebug288410
%patch59 -p1 -b .filter
%patch61 -p1 -b .dot
%patch62 -p1 -b .relro
%patch63 -p1 -b .multilib
%patch64 -p2 -b .type_pun
%patch65 -p1 -b .arm-plasma
%patch66 -p1 -b .klauncher-no-glib
%patch67 -p1 -b .invokeTerminal

# upstream patches
%patch090 -p1 -R -b .return-not-break.-copy-paste-error
%patch091 -p1 -R -b .coding-style-fixes.patch
%patch092 -p1 -R -b .return-application-icons-properly
%patch093 -p1 -R -b .turn-the-packagekit-support-feature-off-by-default

# security fixes
%patch80 -p1 -b .kdelibs-kauth-CVE-2017-8422

# rhel patches
%patch100 -p1 -b .solid-upower099
%patch101 -p1 -b .kdelibs-4.3.4-bz#587016
%if ! 0%{?webkit}
%patch300 -p1 -b .webkit
%endif
%if 0%{?rhel}
%patch301 -p1 -b .abrt
%endif


%build
export CXXFLAGS="$CXXFLAGS -D__STDC_LIMIT_MACROS -D__STDC_CONSTANT_MACROS"
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} \
  -DHUPNP_ENABLED:BOOL=ON \
  -DKAUTH_BACKEND:STRING="PolkitQt-1" \
  -DKDE_DISTRIBUTION_TEXT="%{version}-%{release}%{?fedora: Fedora}%{?rhel: Red Hat Enterprise Linux}" \
  %{?udisks2:-DWITH_SOLID_UDISKS2:BOOL=ON} \
  ..
popd

make %{?_smp_mflags} -C %{_target_platform}

# build apidocs
%if 0%{?apidocs}
export QTDOCDIR="%{?_qt4_docdir}%{?!_qt4_docdir:%(pkg-config --variable=docdir Qt)}"
%if 0%{?apidocs_qch}
export PROJECT_NAME="%{name}"
export PROJECT_VERSION="%{version}%{?alphatag}"
doc/api/doxygen.sh --qhppages .
%else
doc/api/doxygen.sh .
%endif
%endif


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

# see also use-of/patching of XDG_MENU_PREFIX in kdebase/kde-settings
mv %{buildroot}%{_kde4_sysconfdir}/xdg/menus/applications.menu \
   %{buildroot}%{_kde4_sysconfdir}/xdg/menus/kde4-applications.menu

# create/own stuff
# see http://bugzilla.redhat.com/483318
mkdir -p %{buildroot}%{_kde4_libdir}/kconf_update_bin
# own fake mimetype dirs (#907667)
mkdir -p %{buildroot}%{_datadir}/mime/all

## use ca-certificates' ca-bundle.crt, symlink as what most other
## distros do these days (http://bugzilla.redhat.com/521902)
if [  -f %{buildroot}%{_kde4_appsdir}/kssl/ca-bundle.crt -a \
      -f /etc/pki/tls/certs/ca-bundle.crt ]; then
  ln -sf /etc/pki/tls/certs/ca-bundle.crt \
         %{buildroot}%{_kde4_appsdir}/kssl/ca-bundle.crt
fi

# move devel symlinks
mkdir -p %{buildroot}%{_kde4_libdir}/kde4/devel
pushd %{buildroot}%{_kde4_libdir}
for i in lib*.so
do
  case "$i" in
    libkdeinit4_*.so)
      ;;
    *)
      linktarget=`readlink "$i"`
      rm -f "$i"
      ln -sf "../../$linktarget" "kde4/devel/$i"
      ;;
  esac
done
popd

# fix Sonnet documentation multilib conflict
bunzip2 %{buildroot}%{_kde4_docdir}/HTML/en/sonnet/index.cache.bz2
sed -i -e 's!<a name="id[a-z]*[0-9]*"></a>!!g' %{buildroot}%{_kde4_docdir}/HTML/en/sonnet/index.cache
bzip2 -9 %{buildroot}%{_kde4_docdir}/HTML/en/sonnet/index.cache

# install apidocs and generator script
install -p -D doc/api/doxygen.sh %{buildroot}%{_kde4_bindir}/kde4-doxygen.sh

%if 0%{?apidocs}
mkdir -p %{buildroot}%{_kde4_docdir}/HTML/en
cp -a kdelibs-%{version}%{?alphatag}-apidocs %{buildroot}%{_kde4_docdir}/HTML/en/kdelibs4-apidocs
find   %{buildroot}%{_kde4_docdir}/HTML/en/ -name 'installdox' -exec rm -fv {} ';'
rm -vf %{buildroot}%{_kde4_docdir}/HTML/en/kdelibs4-apidocs/*.tmp \
       %{buildroot}%{_kde4_docdir}/HTML/en/kdelibs4-apidocs/index.qhp \
       %{buildroot}%{_kde4_docdir}/HTML/en/kdelibs4-apidocs/*/html/index.qhp

%if 0%{?apidocs_qch}
mkdir -p %{buildroot}%{_qt4_docdir}/qch
for i in %{buildroot}%{_kde4_docdir}/HTML/en/kdelibs4-apidocs/*/qch
do
  mv -f "$i"/* %{buildroot}%{_qt4_docdir}/qch/
  rmdir "$i"
done
%endif
%endif

#the targets are different for each arch, evaluated all at once
mv "%{buildroot}%{_kde4_appsdir}/cmake/modules/KDELibs4LibraryTargets-release.cmake" \
   "%{buildroot}%{_kde4_appsdir}/cmake/modules/KDELibs4LibraryTargets-%{_arch}.cmake"

%if 0%{?hal:1}
install -p -m644 -D %{SOURCE10} %{buildroot}/etc/kde/env/SOLID_HAL_LEGACY.sh
%endif

# this gets installed conditionally if using cmake < 2.8.12.1
# let's just simplify matters and make it unconditional
rm -fv %{buildroot}%{_mandir}/man1/kdecmake.1*

# rpm macros
install -p -m644 -D %{SOURCE1} \
  %{buildroot}%{rpm_macros_dir}/macros.kdelibs4
sed -i \
  -e "s|@@NAME@@|%{name}|g" \
  -e "s|@@EPOCH@@|%{?epoch}%{!?epoch:0}|g" \
  -e "s|@@VERSION@@|%{version}|g" \
  -e "s|@@EVR@@|%{?epoch:%{epoch:}}%{version}-%{release}|g" \
  -e "s|@@KDE_APPLICATIONS_VERSION@@|%{apps_version}|g" \
  %{buildroot}%{rpm_macros_dir}/macros.kdelibs4


%check
%if 0%{?tests}
time xvfb-run -a dbus-launch --exit-with-session make -C %{_target_platform}/ test ARGS="--output-on-failure" ||:
%endif

%post
/sbin/ldconfig
touch --no-create %{_datadir}/mime/packages &> /dev/null || :

%postun
/sbin/ldconfig ||:
if [ $1 -eq 0 ] ; then
  touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null
  gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :
  update-desktop-database -q &> /dev/null
  touch --no-create %{_datadir}/mime/packages &> /dev/null || :
  update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
fi

%posttrans
 gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :
update-desktop-database -q &> /dev/null
update-mime-database %{_datadir}/mime &> /dev/null || :

%files
%doc AUTHORS README TODO
%doc COPYING.LIB
%if 0%{?hal:1}
/etc/kde/env/SOLID_HAL_LEGACY.sh
%endif
%{rpm_macros_dir}/macros.kdelibs4
%{_kde4_bindir}/checkXML
%{_kde4_bindir}/kbuildsycoca4
%{_kde4_bindir}/kcookiejar4
%{_kde4_bindir}/kde4-config
%{_kde4_bindir}/kded4
%{_kde4_bindir}/kdeinit4
%{_kde4_bindir}/kdeinit4_shutdown
%{_kde4_bindir}/kdeinit4_wrapper
%{_kde4_bindir}/kfilemetadatareader
%{_kde4_bindir}/kjs
%{_kde4_bindir}/kjscmd
%{_kde4_bindir}/kmailservice
%{_kde4_bindir}/kross
%{_kde4_bindir}/kshell4
%{_kde4_bindir}/ktelnetservice
%{_kde4_bindir}/kunittestmodrunner
%{_kde4_bindir}/kwrapper4
%{_kde4_bindir}/nepomuk-rcgen
%{_kde4_bindir}/meinproc4
%{_kde4_bindir}/meinproc4_simple
%{_kde4_appsdir}/kauth/
%{_kde4_appsdir}/kcharselect/
%{_kde4_appsdir}/kcm_componentchooser/
%{_kde4_appsdir}/kconf_update/
%{_kde4_appsdir}/kdewidgets/
%{_kde4_appsdir}/khtml/
%{_kde4_appsdir}/kjava/
%{_kde4_appsdir}/knewstuff/
%{_kde4_appsdir}/ksgmltools2/
%{_kde4_appsdir}/kssl/
%{_kde4_appsdir}/LICENSES/
%{_kde4_appsdir}/plasma/
%{_kde4_appsdir}/proxyscout/
%{_kde4_configdir}/accept-languages.codes
%{_kde4_configdir}/khtmlrc
%{_kde4_configdir}/plasmoids.knsrc
%{_datadir}/dbus-1/interfaces/*
%{_sysconfdir}/dbus-1/system.d/*
%{_kde4_datadir}/applications/kde4/kmailservice.desktop
%{_kde4_datadir}/applications/kde4/ktelnetservice.desktop
%{_datadir}/mime/packages/kde.xml
%dir %{_datadir}/mime/all
%{_kde4_sharedir}/kde4/services/*
%{_kde4_sharedir}/kde4/servicetypes/*
%{_kde4_iconsdir}/hicolor/*/*/*
%{_kde4_docdir}/HTML/en/sonnet/
%{_kde4_docdir}/HTML/en/kioslave/
%{_kde4_libdir}/libkcmutils.so.4*
%{_kde4_libdir}/libkde3support.so.4*
%{_kde4_libdir}/libkdeclarative.so.5*
%{_kde4_libdir}/libkdecore.so.5*
%{_kde4_libdir}/libkdefakes.so.5*
%{_kde4_libdir}/libkdesu.so.5*
%{_kde4_libdir}/libkdeui.so.5*
%{_kde4_libdir}/libkdnssd.so.4*
%{_kde4_libdir}/libkemoticons.so.4*
%{_kde4_libdir}/libkfile.so.4*
%{_kde4_libdir}/libkhtml.so.5*
%{_kde4_libdir}/libkidletime.so.4*
%{_kde4_libdir}/libkimproxy.so.4*
%{_kde4_libdir}/libkio.so.5*
%{_kde4_libdir}/libkjsapi.so.4*
%{_kde4_libdir}/libkjsembed.so.4*
%{_kde4_libdir}/libkjs.so.4*
%{_kde4_libdir}/libkmediaplayer.so.4*
%{_kde4_libdir}/libknewstuff2.so.4*
%{_kde4_libdir}/libknewstuff3.so.4*
%{_kde4_libdir}/libknotifyconfig.so.4*
%{_kde4_libdir}/libkntlm.so.4*
%{_kde4_libdir}/libkparts.so.4*
%{_kde4_libdir}/libkprintutils.so.4*
%{_kde4_libdir}/libkpty.so.4*
%{_kde4_libdir}/libkrosscore.so.4*
%{_kde4_libdir}/libkrossui.so.4*
%{_kde4_libdir}/libkunitconversion.so.4*
%{_kde4_libdir}/libkunittest.so.4*
%{_kde4_libdir}/libkutils.so.4*
%{_kde4_libdir}/libnepomukquery.so.4*
%{_kde4_libdir}/libnepomuk.so.4*
%{_kde4_libdir}/libnepomukutils.so.4*
%{_kde4_libdir}/libplasma.so.3*
%{_kde4_libdir}/libsolid.so.4*
%{_kde4_libdir}/libthreadweaver.so.4*
%{_kde4_libdir}/libkdeinit4_*.so
%{_kde4_libdir}/kconf_update_bin/
%dir %{_kde4_libdir}/kde4/
%{_kde4_libdir}/kde4/*.so
%{_kde4_libexecdir}/filesharelist
%{_kde4_libexecdir}/fileshareset
%{_kde4_libexecdir}/kauth-policy-gen
%{_kde4_libexecdir}/kconf_update
%{_kde4_libexecdir}/kdesu_stub
%{_kde4_libexecdir}/kio_http_cache_cleaner
%{_kde4_libexecdir}/kioslave
%{_kde4_libexecdir}/klauncher
# see kio/misc/kpac/README.wpad
%attr(4755,root,root) %{_kde4_libexecdir}/kpac_dhcp_helper
%{_kde4_libexecdir}/ksendbugmail
%{_kde4_libexecdir}/lnusertemp
%{_kde4_libexecdir}/start_kdeinit
%{_kde4_libexecdir}/start_kdeinit_wrapper
%dir %{_kde4_libdir}/kde4/plugins/
%dir %{_kde4_libdir}/kde4/plugins/designer/
%{_kde4_libdir}/kde4/plugins/designer/kde3supportwidgets.so
%{_kde4_libdir}/kde4/plugins/designer/kdedeprecated.so
%{_kde4_libdir}/kde4/plugins/designer/kdewidgets.so
%{_kde4_libdir}/kde4/plugins/imageformats/
%{_kde4_libdir}/kde4/plugins/kauth/
%{_kde4_libdir}/kde4/plugins/script/
%{_kde4_sysconfdir}/xdg/menus/*.menu
%{_mandir}/man1/checkXML.1*
%{_mandir}/man1/kde4-config.1*
%{_mandir}/man1/kjs.1*
%{_mandir}/man1/kjscmd.1*
%{_mandir}/man1/kross.1*
%{_mandir}/man7/kdeoptions.7*
%{_mandir}/man7/qtoptions.7*
%{_mandir}/man8/kbuildsycoca4.8*
%{_mandir}/man8/kcookiejar4.8*
%{_mandir}/man8/kded4.8*
%{_mandir}/man8/kdeinit4.8*
%{_mandir}/man8/meinproc4.8*

%if 0%{?webkit}
%post webkit -p /sbin/ldconfig
%postun webkit -p /sbin/ldconfig

%files webkit
%{_kde4_libdir}/libkdewebkit.so.5*
%{_kde4_libdir}/kde4/plugins/designer/kdewebkitwidgets.so
%endif


%files common
%{_kde4_bindir}/preparetips
%{_kde4_configdir}/colors/
%{_kde4_configdir}/ksslcalist
%{_kde4_configdir}/kdebug.areas
%{_kde4_configdir}/kdebugrc
%{_kde4_configdir}/ui/
%{_kde4_appsdir}/kdeui/
%{_kde4_docdir}/HTML/en/common/
%{_kde4_datadir}/locale/all_languages
%{_kde4_datadir}/locale/en_US/entry.desktop

%files devel
%doc KDE4PORTING.html
%{_mandir}/man1/makekdewidgets.1*
%{_mandir}/man1/kconfig_compiler.1*
%{_mandir}/man1/preparetips.1*
%{_kde4_bindir}/kconfig_compiler4
%{_kde4_bindir}/makekdewidgets4
%{_kde4_bindir}/plasma-dataengine-depextractor
%{_kde4_bindir}/kde4-doxygen.sh
%{_kde4_appsdir}/cmake/
%{_kde4_includedir}/*
%{_kde4_libdir}/cmake/KDeclarative/
%{_kde4_libdir}/kde4/devel/

%if 0%{?webkit}
%exclude %{_kde4_includedir}/kdewebkit_export.h
%exclude %{_kde4_includedir}/kgraphicswebview.h
%exclude %{_kde4_includedir}/kwebpage.h
%exclude %{_kde4_includedir}/kwebpluginfactory.h
%exclude %{_kde4_includedir}/kwebview.h
%exclude %{_kde4_includedir}/kwebwallet.h
%exclude %{_kde4_libdir}/kde4/devel/libkdewebkit.so

%files webkit-devel
%{_kde4_includedir}/kdewebkit_export.h
%{_kde4_includedir}/kgraphicswebview.h
%{_kde4_includedir}/kwebpage.h
%{_kde4_includedir}/kwebpluginfactory.h
%{_kde4_includedir}/kwebview.h
%{_kde4_includedir}/kwebwallet.h
%{_kde4_libdir}/kde4/devel/libkdewebkit.so
%endif

%post ktexteditor -p /sbin/ldconfig
%postun ktexteditor -p /sbin/ldconfig

%files ktexteditor
%{_kde4_libdir}/libktexteditor.so.4*


%if 0%{?apidocs}
%files apidocs
%{_kde4_docdir}/HTML/en/kdelibs4-apidocs/

%if 0%{?apidocs_qch}
%files apidocs-qch
%{_qt4_docdir}/qch/*.qch
%endif
%endif


%changelog
* Thu May 18 2017 Jan Grulich <jgrulich@redhat.com> - 6:4.14.8-6
- KAuth: verify that whoever is calling us is actually who he says he is (CVE-2017-8422)
  Resolves: CVE-2017-8422

* Tue Feb 02 2016 Jan Grulich <jgrulich@redhat.com> - 6:4.14.8-5
- Fix required kde-runtime version in macros.kdelibs4
  Resolves: bz#1289241

* Tue Jul 21 2015 Jan Grulich <jgrulich@redhat.com> - 6:4.14.8-4
- Restore old patch for proper restoring of print setting
  Resolves: bz#1197804

* Fri Jun 05 2015 Jan Grulich <jgrulich@redhat.com> - 6:4.14.8-3
- Drop nepomuk subpackages

* Wed May 27 2015 Jan Grulich <jgrulich@redhat.com> - 6:4.14.8-2
- Rebuild, we need also aarch64 build

* Mon May 25 2015 Jan Grulich <jgrulich@redhat.com> - 6:4.14.8-1
- Re-base to 4.14.8 (sync with F21)

* Mon Apr 13 2015 Lukáš Tinkl <ltinkl@redhat.com> - 6:4.10.5-7
- Resolves: #1202801 - Backport patch to with upower 1.0 API

* Tue Jan 28 2014 Daniel Mach <dmach@redhat.com> - 6:4.10.5-6
- Mass rebuild 2014-01-24

* Wed Jan 08 2014 Martin Briza <mbriza@redhat.com> - 4.10.5-5
- fixed a typo in Summary
- removed an unused patch
- Resolves: #884052

* Wed Jan 08 2014 Martin Briza <mbriza@redhat.com> - 4.10.5-4
- use a better way to figure out if lib or lib64 should be used
- use -fno-strict-aliasing for type punned source files
- Resolves: #884052

* Wed Jan 08 2014 Martin Briza <mbriza@redhat.com> - 4.10.5-3
- make kpac_dhcp_helper full relro
- set the variables in the generated cmake files to contain both 64b and 32b paths
- hide "command not found" for one pkg-config invocation in the spec
- fix macro expansion in the spec changelog
- Resolves: #884052

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 6:4.10.5-2
- Mass rebuild 2013-12-27

* Sun Jun 30 2013 Than Ngo <than@redhat.com> - 4.10.5-1
- 4.10.5

* Sat Jun 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 6:4.10.4-1
- 4.10.4

* Thu May 09 2013 Rex Dieter <rdieter@fedoraproject.org> - 6:4.10.3-2
- pull in a few upstream fixes, including a couple minor security issues
- Crash in DialogShadows::Private::freeX11Pixmaps() (kde#319137)

* Mon May 06 2013 Than Ngo <than@redhat.com> - 6:4.10.1-1
- 4.10.3

* Tue Apr 30 2013 Than Ngo <than@redhat.com> - 6:4.10.2-4
- drop old kdelibs-4.1.72-no-cache-kdeglobals-paths.patch

* Wed Apr 24 2013 Rex Dieter <rdieter@fedoraproject.org> 6:4.10.2-3
- fix/workaround plasma-desktop crash (kde#318806)
- respin FindSamba patch

* Tue Apr 16 2013 Rex Dieter <rdieter@fedoraproject.org> 6:4.10.2-2
- revert upstream commit wrt icon inheritance, for now, to avoid regression (kde#317138)

* Sat Mar 30 2013 Rex Dieter <rdieter@fedoraproject.org> 6:4.10.2-1
- 4.10.2

* Thu Mar 21 2013 Rex Dieter <rdieter@fedoraproject.org> 6:4.10.1-3
- lower strigi min version
- BR: cmake >= 2.8.9
- minor tweaks for el6 (hal!)

* Sun Mar 10 2013 Rex Dieter <rdieter@fedoraproject.org> 6:4.10.1-2
- rebuild (OpenEXR)

* Sat Mar 02 2013 Rex Dieter <rdieter@fedoraproject.org> - 6:4.10.1-1
- 4.10.1

* Thu Feb 28 2013 Than Ngo <than@redhat.com> - 6:4.10.0-4
- rhel condition:
    adapt webkit patch
    abrt by default
    disable dot to reduce doc size

* Thu Feb 07 2013 Lukáš Tinkl <ltinkl@redhat.com> 6:4.10.0-3
- complete kdelibs-udisks2_2_stage.patch

* Tue Feb 05 2013 Rex Dieter <rdieter@fedoraproject.org> 6:4.10.0-2
- kdelibs-udisks2_2_stage.patch (fix for some phones/mtp-device detection)

* Thu Jan 31 2013 Rex Dieter <rdieter@fedoraproject.org> - 6:4.10.0-1
- 4.10.0

* Sat Jan 19 2013 Rex Dieter <rdieter@fedoraproject.org> - 6:4.9.98-1
- 4.9.98

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 6:4.9.97-2
- rebuild due to "jpeg8-ABI" feature drop

* Thu Jan 03 2013 Rex Dieter <rdieter@fedoraproject.org> - 6:4.9.97-1
- 4.9.97

* Sat Dec 29 2012 Rex Dieter <rdieter@fedoraproject.org> 6:4.9.95-3
- FindKdcraw.cmake fixes(kde#311936)

* Thu Dec 20 2012 Rex Dieter <rdieter@fedoraproject.org> 6:4.9.95-2
- Conflicts: kdelibs3 < 3.5.10-42

* Wed Dec 19 2012 Rex Dieter <rdieter@fedoraproject.org> - 6:4.9.95-1
- 4.9.95

* Thu Dec 13 2012 Rex Dieter <rdieter@fedoraproject.org> 6:4.9.90-4
- prune/fix changelog

* Wed Dec 12 2012 Rex Dieter <rdieter@fedoraproject.org> 6:4.9.90-3
- fix udisks2 conditional, so -DWITH_SOLID_UDISKS2:BOOL=ON really gets set

* Wed Dec 12 2012 Rex Dieter <rdieter@fedoraproject.org> - 6:4.9.90-2
- sync with latest solid/udisks2 upstream bits
- Debug output in kdelibs-udisks2-backend.patch should be disabled (#882731)

* Mon Dec 03 2012 Rex Dieter <rdieter@fedoraproject.org> 6:4.9.90-1
- 4.9.90 (4.10beta2)

* Mon Dec 03 2012 Than Ngo <than@redhat.com> - 6:4.9.4-1
- 4.9.4
- update udisks2 backend patch to fix ghost devices

* Fri Nov 30 2012 Dan Vrátil <dvratil@redhat.com> - 6:4.9.3-7
- update udisks2 backend patch

* Thu Nov 29 2012 Than Ngo <than@redhat.com> - 6:4.9.3-6
- fix file filter

* Thu Nov 29 2012 Lukáš Tinkl <ltinkl@redhat.com> 6:4.9.3-5
- update udisks2 backend patch

* Fri Nov 23 2012 Jan Grulich <jgrulich@redhat.com> 6:4.9.3-4
- Fix previous patch

* Fri Nov 23 2012 Jan Grulich <jgrulich@redhat.com> 6:4.9.3-3
- Resolves: bz#877021

* Fri Nov 02 2012 Rex Dieter <rdieter@fedoraproject.org> 6:4.9.3-2
- (re)enable apidocs

* Fri Nov 02 2012 Rex Dieter <rdieter@fedoraproject.org> 6:4.9.3-1
- 4.9.3

* Wed Oct 31 2012 Than Ngo <than@redhat.com> - 6:4.9.2-11
- Resolves: CVE-2012-4514

* Wed Oct 31 2012 Than Ngo <than@redhat.com> - 6:4.9.2-10
- Resolves: bz#871541, CVE-2012-4515

* Mon Oct 29 2012 Lukáš Tinkl <ltinkl@redhat.com> 6:4.9.2-9
- Resolves #868530 - cache information about solid device in 'Places'
  panel in  open/save dialog
- update solid/udisks2 backend, switch to cmake-define

* Thu Oct 25 2012 Dan Vrátil <dvratil@redhat.com> 6:4.9.2-8
- Resolves #868530 - cache information about solid device in 'Places'
  panel in  open/save dialog

* Wed Oct 24 2012 Rex Dieter <rdieter@fedoraproject.org> 6:4.9.2-7
- rebuild (libjpeg-turbo v8)

* Mon Oct 08 2012 Rex Dieter <rdieter@fedoraproject.org> 6:4.9.2-6
- cmake/python3 love (kde#275919)

* Thu Oct 04 2012 Rex Dieter <rdieter@fedoraproject.org> 6:4.9.2-5
- multilib conflict /usr/share/doc/HTML/en/sonnet/index.cache.bz2 (#862388)

* Thu Oct 04 2012 Than Ngo <than@redhat.com> - 6:4.9.2-4
- revert kde#108510, kde#183534

* Tue Oct 02 2012 Rex Dieter <rdieter@fedoraproject.org> 6:4.9.2-3
- patch FindSamba.cmake to use pkg-config hints (#862169)

* Sat Sep 29 2012 Rex Dieter <rdieter@fedoraproject.org> 6:4.9.2-2
- respin

* Fri Sep 28 2012 Rex Dieter <rdieter@fedoraproject.org> - 6:4.9.2-1
- 4.9.2

* Wed Sep 26 2012 Rex Dieter <rdieter@fedoraproject.org> 6:4.9.1-5
- respin FindKipi.cmake patch (kde#307213)

* Sat Sep 22 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> - 6:4.9.1-4
- actually enable Solid udisks2 backend (restore patch hunks lost in 4.9.1-2)
- backport FindKipi.cmake from Digikam SC 3.0.0-beta1 for libkipi 2 (kde#307213)

* Wed Sep 19 2012 Lukas Tinkl <ltinkl@redhat.com> - 6:4.9.1-3
- Resolves #690123 - solid-udisks: Constant spinning of DVD drive when
  selecting dolphin

* Tue Sep 04 2012 Lukas Tinkl <ltinkl@redhat.com> - 6:4.9.1-2
- rebase udisks2 backend against KDE/4.10 branch

* Mon Sep 03 2012 Than Ngo <than@redhat.com> - 6:4.9.1-1
- 4.9.1

* Wed Aug 29 2012 Rex Dieter <rdieter@fedoraproject.org> 6:4.9.0-4
- Can't safely remove a USB removable hard drive (#852196)

* Sun Aug 12 2012 Rex Dieter <rdieter@fedoraproject.org> - 6:4.9.0-3
- drop .spec cruft
- Requires: media-player-info

* Thu Aug 02 2012 Rex Dieter <rdieter@fedoraproject.org> 6:4.9.0-2
- respin

* Thu Jul 26 2012 Lukas Tinkl <ltinkl@redhat.com> - 6:4.9.0-1
- 4.9.0

* Sun Jul 22 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> - 6:4.8.97-7
- revert "-devel: move only conflicting lib symlinks to kde4/devel" (#842142)

* Sat Jul 21 2012 Rex Dieter <rdieter@fedoraproject.org> - 6:4.8.97-6
- -devel: move only conflicting lib symlinks to kde4/devel
- drop old Conflicts/Obsoletes

* Wed Jul 18 2012 Lukas Tinkl <ltinkl@redhat.com> - 6:4.8.97-5
- respin the udisks2 backend patch
- fix k3b not recognizing any CD/DVD burning device

* Fri Jul 13 2012 Rex Dieter <rdieter@fedoraproject.org> - 6:4.8.97-4
- CD drive tray goes back in after 'Eject' when dolphin is running (kde#296657, #811609)

* Thu Jul 12 2012 Rex Dieter <rdieter@fedoraproject.org> - 6:4.8.97-3
- provide /usr/bin/kmailservice (#773414)

* Thu Jul 12 2012 Than Ngo <than@redhat.com> - 6:4.8.97-2
- fix kjs to return valid lang (RFC 1766)

* Wed Jul 11 2012 Rex Dieter <rdieter@fedoraproject.org> - 6:4.8.97-1
- 4.8.97

* Wed Jun 27 2012 Lukas Tinkl <ltinkl@redhat.com> - 6:4.8.95-2
- respin the udisks2 backend patch
- Resolves #835107 - Unable to eject optical media using "Device
  notifier"

* Wed Jun 27 2012 Radek Novacek <rnovacek@redhat.com> - 6:4.8.95-1
- 4.8.95

* Tue Jun 26 2012 Lukáš Tinkl <ltinkl@redhat.com> - 6:4.8.90-4
- update the udisks2 backend patch


* Wed Jun 20 2012 Rex Dieter <rdieter@fedoraproject.org> 6:4.8.90-3
- rebuild (attica)

* Sat Jun 09 2012 Rex Dieter <rdieter@fedoraproject.org> 6:4.8.90-2
- rebuild

* Fri Jun 08 2012 Jaroslav Reznik <jreznik@redhat.com> - 6:4.8.90-1
- 4.8.90

* Fri Jun 01 2012 Jaroslav Reznik <jreznik@redhat.com> - 6:4.8.80-2
- respin

* Fri May 25 2012 Jaroslav Reznik <jreznik@redhat.com> - 6:4.8.80-1
- 4.8.80

* Fri May 25 2012 Rex Dieter <rdieter@fedoraproject.org>
- 6:4.8.3-4
- include upstream kmessagewidget fixes
- apply kdeclarative-install-location.patch

* Thu May 24 2012 Lukas Tinkl <ltinkl@redhat.com> - 6:4.8.3-3
- update the udisks2 backend patch, fixing some bugs with storage drives

* Thu May 03 2012 Than Ngo <than@redhat.com> - 6:4.8.3-2
- add rhel/fedora condition

* Mon Apr 30 2012 Jaroslav Reznik <jreznik@redhat.com> - 6:4.8.3-1
- 4.8.3
- remove cmake implicit link directories patch
- remove adblock filter patch
- add kdeclarative install location patch

* Mon Apr 16 2012 Rex Dieter <rdieter@fedoraproject.org> 6:4.8.2-4
- enable udisks2, +Requires: udisks2 on f18+ too

* Mon Apr 16 2012 Lukas Tinkl <ltinkl@redhat.com> - 6:4.8.2-3
- add udisks2 Solid backend plus RHEL conditional

* Thu Apr 12 2012 Than Ngo <than@redhat.com> - 6:4.8.2-2
- Load/Update filter lists only when AdBlock is enabled

* Fri Mar 30 2012 Jaroslav Reznik <jreznik@redhat.com> - 6:4.8.2-1
- 4.8.2

* Thu Mar 22 2012 Jaroslav Reznik <jreznik@redhat.com> 6:4.8.1-3
- Sonnet crash due to unitialized value access (kde#295615, rhbz#805010)

* Tue Mar 13 2012 Rex Dieter <rdieter@fedoraproject.org> 6:4.8.1-2
- Nepomuk::Resource[Data|Watcher] thread-safety (kde#295474)

* Mon Mar 05 2012 Radek Novacek <rnovacek@redhat.com> 6:4.8.1-1
- 4.8.1
- Drop upstreamed patches

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6:4.8.0-5
- Rebuilt for c++ ABI breakage

* Sat Feb 18 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8.0-4
- don't set rpath on multiarch dirs (kde review request #103422)

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 6:4.8.0-3
- Rebuild against PCRE 8.30

* Sat Feb 04 2012 Rex Dieter <rdieter@fedoraproject.org> 6:4.8.0-2
- fix KDE_VERSION_STRING (kde#293204)

* Thu Jan 19 2012 Jaroslav Reznik <jreznik@redhat.com> - 6:4.8.0-1
- 4.8.0

* Wed Jan 04 2012 Radek Novacek <rnovacek@redhat.com> - 6:4.7.97-1
- 4.7.97

* Sat Dec 31 2011 Rex Dieter <rdieter@fedoraproject.org> 6:4.7.95-2
- rebuild (attica)

* Wed Dec 21 2011 Radek Novacek <rnovacek@redhat.com> - 6:4.7.95-1
- 4.7.95
- drop patch for Plasma::PackageMetadata::read: Match the behavior of KService.

* Tue Dec 06 2011 Than Ngo <than@redhat.com> - 4.7.90-2
- add ss390/s390x support in kjs

* Sat Dec 03 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.90-1
- 4.7.90

* Thu Dec 01 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.80-3
- disable solid/upnp by default, set env SOLID_UPNP=1 to re-enable (#754530, #758008, kde#259472)

* Tue Nov 29 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.80-2
- drop kactivities conditional

* Fri Nov 18 2011 Jaroslav Reznik <jreznik@redhat.com> 4.7.80-1
- 4.7.80 (beta 1)

* Wed Nov 16 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.3-5
- restore halectomy patch (sans fstab-removing pieces)

* Mon Nov 14 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.3-4
- solid hardware does not detect NFS drives, halectomy related (#751879)

* Mon Nov 07 2011 Than Ngo <than@redhat.com> - 4.7.3-3
- CVE-2010-0046, security issue in khtml

* Fri Nov 04 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.3-2
- no_libkactivities

* Sat Oct 29 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.3-1
- 4.7.3

* Thu Oct 27 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.2-5
- omit knotify hack, fix in qt instead

* Wed Oct 26 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.2-4
- fix knotify, workaround Qt 4.8 QUrl.toLocalFile behavior change (#749213)

* Tue Oct 25 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.2-3
- no_libkactivities toggle, -devel: Provides: libkactivities-devel

* Sun Oct 09 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.2-2
- upstream nepomuk_unicode patch

* Tue Oct 04 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.2-1
- 4.7.2

* Tue Oct 04 2011 Lukas Tinkl <ltinkl@redhat.com> - 4.7.1-6
- Resolves #743056 - CVE-2011-3365 kdelibs: input validation failure in KSSL

* Wed Sep 28 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.1-5
- -devel: s/pkgconfig(attica)/pkgconfig(libattica)/

* Tue Sep 27 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.7.1-4
- updated Plasma data engine dependency extraction patch:
  - added support for declarativeappletscript QML code
  - plasma-dataengine-depextractor command-line tool:
    - make sure we pass an absolute path to KDesktopFile
    - autodetect the API/language used, drop --api command-line argument

* Thu Sep 22 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.1-3
- pkgconfig-style deps
- move kde4_appsdir/kdewidgets to main pkg (pairs with kdewidgets designer plugin)

* Fri Sep 02 2011 Than Ngo <than@redhat.com> - 4.7.1-1
- 4.7.1

* Tue Aug 30 2011 Than Ngo <than@redhat.com> - 4.7.0-5
- clean up fedora conditonals

* Mon Aug 22 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.7.0-4
- fix Plasma::PackageMetadata::read to match the behavior of KService

* Sun Aug 21 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.7.0-3
- backport my GSoC 2011 patches for libplasma PackageKit integration (F17+)
- package plasma-dataengine-depextractor in -devel (F17+)

* Sun Aug 21 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.7.0-2
- rebuild for the RPM dependency generators for Plasma (GSoC 2011)
- add BuildRequires: kde-settings to pick up the above

* Tue Jul 26 2011 Jaroslav Reznik <jreznik@redhat.com> 4.7.0-1
- 4.7.0

* Mon Jul 25 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.6.95-11
- fix KHTML form completion regression (kde#277457, patch by Andrea Iacovitti)

* Fri Jul 22 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.95-10
- drop kate

* Thu Jul 21 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.95-4
- rebuild (qt48)

* Wed Jul 20 2011 Jaroslav Reznik <jreznik@redhat.com> 4.6.95-3
- add Herqq dependency for Solid's UPnP support

* Fri Jul 08 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.95-2
- drop upstreamed qt48 patch
- Provides: katepart

* Fri Jul 08 2011 Jaroslav Reznik <jreznik@redhat.com> 4.6.95-1
- 4.6.95 (rc2)

* Thu Jun 30 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.90-4
- drop unneeded kstatusnotify_dbus_leak.patch (upstream fixed better)

* Wed Jun 29 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.90-3
- fix %%shared_desktop_ontologies_ver(sion) usage
- upstream kdoctools/docbook patch (#690124)

* Tue Jun 28 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.90-2
- move oxygen-icons-theme dep (back) to kdebase-runtime

* Mon Jun 27 2011 Than Ngo <than@redhat.com> - 4.6.90-1
- 4.6.90 (rc1)

* Tue Jun 14 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.80-5
- KStatusNotifierItem leaks D-Bus connections (#667787, kde#261180)

* Sun Jun 12 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.6.80-4
- rebuild for new qtwebkit (in an attempt to fix KWebPage crash)

* Thu Jun 02 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.80-3
- up min versions of phonon, shared-desktop-ontologies, soprano

* Thu Jun 02 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.6.80-2
- fix KConfigXT KComboBox for Qt 4.8 TP1 (upstream patch)

* Fri May 27 2011 Jaroslav Reznik <jreznik@redhat.com> 4.6.80-1
- 4.6.80 (beta1)

* Tue May 24 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.6.3-5
- fix kio regression causing requests submitted twice (#707146, kde#272466)

* Mon May 16 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.3-4.1
- Requires: oxygen-icon-theme >= 4.6.2

* Tue May 10 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.6.3-4
- Apply the xdg-menu patch everywhere again (#703531)
- Requires: redhat-menus (proper fix for #701693)

* Sun May 08 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.3-3
- Plasma crash in KiconLoader (kde258706)

* Tue May 03 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.6.3-2
- Drop xdg-menu patch on F15+ (#701693)

* Thu Apr 28 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.3-1
- 4.6.3

* Mon Apr 25 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.2-3
- Adjust uri/ mimetypes to use newer x-scheme-handler/ (#587573)

* Tue Apr 19 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.2-2
- Solid::Networking::status() returning Solid::Networking::Status::Unknown (kde#270538)

* Wed Apr 06 2011 Jaroslav Reznik <jreznik@redhat.com> 4.6.2-1
- 4.6.2

* Wed Mar 23 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.1-5
- Constant spinning of cd/dvd drive ... (#690123, kde#264487)

* Fri Mar 11 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.6.1-4
- use upstream patch for #682300 (kde#267770), my previous one didn't work

* Fri Mar 11 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.6.1-3
- set the plugin path in KApplication, don't rely on QT_PLUGIN_PATH being set,
  fixes kpackagekitsmarticon not getting themed (#682300, kde#267770)

* Tue Mar 08 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.1-2
- Dolphin shows no files... (kde#267709)

* Sat Feb 26 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.1-1
- 4.6.1

* Mon Feb 21 2011 Jaroslav Reznik <jreznik@redhat.com> - 4.6.0-4
- Fix plasma logout crash (kde#264076)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6:4.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 25 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.6.0-2
- Conflicts with old versions of kdevplatform, kdevelop, kile, rkward to force
  their upgrade to compatible versions

* Fri Jan 21 2011 Jaroslav Reznik <jreznik@redhat.com> - 4.6.0-1
- 4.6.0

* Tue Jan 18 2011 Rex Dieter <rdieter@fedoraproject.org> - 4.5.95-2
- Unowned /usr/lib*/kde4/plugins/{gui_platform,styles} dirs (#645059)

* Wed Jan 05 2011 Jaroslav Reznik <jreznik@redhat.com> - 4.5.95-1
- 4.5.95 (4.6rc2)

* Mon Jan 03 2011 Lukas Tinkl <ltinkl@redhat.com> - 4.5.90-3
- update the halectomy patch to also omit the fstab backend
  (may interfere with the udisks backend, causing deadlocks, cf kdebug#261359)

* Thu Dec 23 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5.90-2
- build hal-free (ltinkl)

* Wed Dec 22 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5.90-1
- 4.5.90 (4.6rc1)

* Fri Dec 17 2010 Jaroslav Reznik <jreznik@redhat.com> - 4.5.85-5
- rebuild for polkit-qt-1-0.99.0 (soname 1.99.0)

* Fri Dec 10 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.5.85-4
- -common: Conflicts: kdebase-runtime < 4.5.80
- drop some old pre-f13 era Conflicts

* Fri Dec 10 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.5.85-3
- fix FindQt4.cmake when there's also qt3-devel installed (#661996)

* Wed Dec 08 2010 Thomas Janssen <thomasj@fedoraproject.org> 4.5.85-2
- respun upstream tarball

* Fri Dec 03 2010 Thomas Janssen <thomasj@fedoraproject.org> 4.5.85-1
- 4.5.85 (4.6beta2)

* Fri Nov 26 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5.80-7
- move udisks/upower dep to main pkg (from -devel)

* Wed Nov 24 2010 Lukas Tinkl <ltinkl@redhat.com> - 4.5.80-6
- explicitely require udisks/upower now that we depend on them

* Tue Nov 23 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.5.80-5
- respun tarball (again), includes fix-build patch

* Tue Nov 23 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.5.80-4
- respun tarball
- fix build failure triggered by "build fix" (patch by Jonathan Riddell)

* Mon Nov 22 2010 Lukas Tinkl <ltinkl@redhat.com> - 4.5.80-3
- don't build Solid HAL backend, rely on udisks/upower/udev only
  (aka project HALsectomy)

* Sat Nov 20 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.5.80-2
- squash more rpath's

* Sat Nov 20 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.5.80-1
- 4.5.80 (4.6beta1)

* Mon Nov 15 2010 Rex Dieter <rdieter@fedoraproject.org> -  4.5.3-3
- Closing a konsolepart shell crashes (kde#256652)

* Fri Nov 05 2010 Thomas janssen <thomasj@fedoraproject.org> 4.5.3-2
- rebuild for new libxml2

* Fri Oct 29 2010 Than Ngo <than@redhat.com> - 4.5.3-1
- 4.5.3

* Fri Oct 15 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.5.2-7
- backport configChanged() for wallpaper

* Fri Oct 15 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.5.2-6
- kio/krun patch so kde services can open urls directly too

* Fri Oct 08 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.5.2-5
- switching comic in comic applet crashes plasma (kde#253387,rh#640619)

* Thu Oct 07 2010 Than Ngo <than@redhat.com> - 4.5.2-4
- kde253294, KMail and Kopete download and open https url instead of only opening

* Tue Oct 05 2010 Lukas Tinkl <ltinkl@redhat.com> - 4.5.2-3
- tarball respin

* Fri Oct 01 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5.2-2
- rebuild (phonon)

* Fri Oct 01 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5.2-1
- 4.5.2

* Fri Sep 10 2010 Thomas Janssen <thomasj@fedoraproject.org> 4.5.1-4
- backport patches to fix a crashing kdevelop (kde 4.5.1 only)

* Fri Aug 27 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.5.1-3
- make building -apidocs-qch optional and disable it by default until fixed

* Fri Aug 27 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.5.1-2
- -apidocs : exclude installdox

* Fri Aug 27 2010 Jaroslav Reznik <jreznik@redhat.com> - 4.5.1-1
- 4.5.1
- use gpg2 in knewstuff (kde#249152)

* Thu Aug 26 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.5.0-6
- use ca-certificates' ca-bundle.crt  (#521902)

* Wed Aug 18 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.5.0-5
- fix packaging of QCH apidocs

* Wed Aug 18 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.5.0-4
- package QCH apidocs (-apidocs-qch noarch subpackage)

* Wed Aug 18 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.5.0-3
- generate QCH apidocs (try 1)

* Tue Aug 10 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.5.0-2
- (Build)Requires: qt4(-devel) >= 4.6.3
- dbusmenu_qt_ver 0.5.2, soprano_ver 4.5.0

* Tue Aug 03 2010 Than Ngo <than@redhat.com> - 4.5.0-1
- 4.5.0

* Sun Jul 25 2010 Rex Dieter <rdieter@fedoraproject.org> - 6:4.4.95-1
- 4.5 RC3 (4.4.95)

* Wed Jul 21 2010 Than Ngo <than@redhat.com> - 6:4.4.92-4
- (Build)Requires: qt4(-devel) >= 4.7.0
- drop icon-name-qt47 patch

* Fri Jul 16 2010 Rex Dieter <rdieter@fedoraproject.org> - 6:4.4.92-3
- Requires: oxygen-icon-theme (ensures default fallback is present)

* Wed Jul 07 2010 Rex Dieter <rdieter@fedoraproject.org> - 6:4.4.92-2
- tarball respin

* Wed Jul 07 2010 Rex Dieter <rdieter@fedoraproject.org> - 6:4.4.92-1
- 4.5 RC2 (4.4.92)

* Fri Jun 25 2010 Jaroslav Reznik <jreznik@redhat.com> - 6:4.4.90-1
- 4.5 RC1 (4.4.90)

* Thu Jun 17 2010 Rex Dieter <rdieter@fedoraproject.org> - 6:4.4.85-3
- Plasma crash on startup (kde#241298)

* Tue Jun 08 2010 Jaroslav Reznik <jreznik@redhat.com> - 6:4.4.85-2
- (Build)Requires: docbook-dtds, docbook-style-xsl
- drop fedora < 12 conditionals

* Mon Jun 07 2010 Jaroslav Reznik <jreznik@redhat.com> - 6:4.4.85-1
- 4.5 Beta 2 (4.4.85)

* Tue May 25 2010 Rex Dieter <rdieter@fedoraproject.org> - 6:4.4.80-3
- Blur shadow around widgets does not smoothly fade out (kde#235620)

* Sun May 23 2010 Rex Dieter <rdieter@fedoraproject.org> - 6:4.4.80-2
- own %%{_kde4_libdir}/plugins/{gui_platform,styles}

* Fri May 21 2010 Jaroslav Reznik <jreznik@redhat.com> - 6:4.4.80-1
- 4.5 Beta 1 (4.4.80)
- BuildRequires: dbusmenu-qt-devel

* Sun May 16 2010 Rex Dieter <rdieter@fedoraproject.org> 6:4.4.3-5
- Web proxy auto-discovery (WPAD) fails (#592658)

* Sat May 08 2010 Rex Dieter <rdieter@fedoraproject.org> 6:4.4.3-4
- -devel: Req: qt4-webkit-devel

* Sat May 08 2010 Rex Dieter <rdieter@fedoraproject.org> 6:4.4.3-3
- BR: qt4-webkit-devel

* Wed May 05 2010 Than Ngo <than@redhat.com> - 6:4.4.3-2
- respin

* Fri Apr 30 2010 Jaroslav Reznik <jreznik@redhat.com> - 6:4.4.3-1
- 4.4.3

* Sun Apr 25 2010 Rex Dieter <rdieter@fedoraproject.org> - 6:4.4.2-5
- rebuild (soprano)

* Sat Apr 24 2010 Rex Dieter <rdieter@fedoraproject.org> - 6:4.4.2-4
- fix kidletime (kde#231628,kde#227279,kde#218468)
- kate part ignores japanese input from input method (#585242,kde#206455)

* Thu Apr 15 2010 Rex Dieter <rdieter@fedoraproject.org> - 6:4.4.2-3
- cleanup/fix webkitkde Obsoletes a bit more (#582469)
- (Build)Requies: cmake >= 2.6.4

* Fri Apr 09 2010 Rex Dieter <rdieter@fedoraproject.org> - 6:4.4.2-2
- Obsoletes: webkitkde < 0.0.6 (#576634)

* Mon Mar 29 2010 Lukas Tinkl <ltinkl@redhat.com> - 6:4.4.2-1
- 4.4.2

* Thu Mar 25 2010 Rex Dieter <rdieter@fedoraproject.org> 6:4.4.1-10
- drop BR: openssh-clients subversion

* Thu Mar 25 2010 Rex Dieter <rdieter@fedoraproject.org> 6:4.4.1-9
- refresh kdelibs-4.4.2-kpixmapcache.patch

* Wed Mar 24 2010 Rex Dieter <rdieter@fedoraproject.org> 6:4.4.1-8
- Obsoletes: webkitkde (#576634)

* Sat Mar 20 2010 Rex Dieter <rdieter@fedoraproject.org> 6:4.4.1-7
- KDE default in noisy debug mode to stdout/stderr (kde#227089)
- backport trunk/ fix building against qt-4.7

* Wed Mar 17 2010 Lukas Tinkl <ltinkl@redhat.com> - 6:4.4.1-6
- fix crash in KPixmapCache (bug#568389)

* Tue Mar 09 2010 Rex Dieter <rdieter@fedoraproject.org> - 6:4.4.1-5
- rebuild (soprano)

* Tue Mar 09 2010 Rex Dieter <rdieter@fedoraproject.org> - 6:4.4.1-4
- Requires: hal (for solid)
- drop Requires: dbus-x11 (it's already Req'd in kdebase-workspace)
- drop Requires: coreutils grep (F-12+)
- make Requires: kdelibs-common versioned

* Sun Feb 28 2010 Rex Dieter <rdieter@fedoraproject.org> - 6:4.4.1-3
- put back CMAKE_INSTALL_RPATH_USE_LINK_PATH FALSE to avoid
  %%_libdir/kde/devel rpaths (#568495)

* Sun Feb 28 2010 Rex Dieter <rdieter@fedoraproject.org> - 6:4.4.1-2
- update no_rpath patch, revert back to
  CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE (#568495)

* Sat Feb 27 2010 Rex Dieter <rdieter@fedoraproject.org> - 6:4.4.1-1
- 4.4.1

* Fri Feb 19 2010 Rex Dieter <rdieter@fedoraproject.org> - 6:4.4.0-9
- -devel: Provides: nepomuk-devel, Requires: soprano-devel

* Tue Feb 16 2010 Than Ngo <than@redhat.com> - 6:4.4.0-8
- krunner crash patch (kde#227118)
- plasma crash patch (kde#226823)

* Sat Feb 13 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 6:4.4.0-7
- rebuild for new kde-filesystem in F13, fixes kde4-config --libsuffix (#564712)

* Sat Feb 13 2010 Rex Dieter <rdieter@fedoraproject.org> - 6:4.4.0-6
- nepomuk_memleak patch

* Fri Feb 12 2010 Rex Dieter <rdieter@fedoraproject.org> - 6:4.4.0-5
- khtml_scrolling patch
- drop khtml_svg_no_var_tracking_assignments patch

* Tue Feb 09 2010 Rex Dieter <rdieter@fedoraproject.org> - 6:4.4.0-4
- depend on version of phonon,strigi,soprano built against

* Tue Feb 09 2010 Rex Dieter <rdieter@fedoraproject.org> - 6:4.4.0-3
- respin

* Mon Feb 08 2010 Rex Dieter <rdieter@fedoraproject.org> - 6:4.4.0-2
- respin

* Fri Feb 05 2010 Than Ngo <than@redhat.com> - 6:4.4.0-1
- 4.4.0

* Tue Feb 02 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.3.98-4
- -apidocs: build as normal noarch subpkg

* Tue Feb 02 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.3.98-3
- respin no_rpath patch, add LIB_INSTALL_DIR rpath only if not in
  CMAKE_SYSTEM_LIBRARY_PATH.  added some status messages to help debug.

* Mon Feb 01 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.3.98-2
- no_rpath patch, goodbye -DCMAKE_SKIP_RPATH:BOOL=ON, it's been fun

* Sun Jan 31 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.3.98-1
- KDE 4.3.98 (4.4rc3)

* Wed Jan 27 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.3.95-3
- patch for kde4-config --kde-version option (kde#224540)

* Tue Jan 26 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.3.95-2
- -devel: Obsoletes: webkitkde-devel

* Wed Jan 20 2010 Lukas Tinkl <ltinkl@redhat.com> - 4.3.95-1
- KDE 4.3.95 (4.4rc2)

* Thu Jan 14 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.3.90-6
- use %%_polkit_qt_policydir
- strigi_ver 0.7.1

* Mon Jan 11 2010 Jaroslav Reznik <jreznik@redhat.com> - 4.3.90-5
- hopefully correct kauth fix (old polkit cmake module is broken)

* Fri Jan 08 2010 Jaroslav Reznik <jreznik@redhat.com> - 4.3.90-4
- fix kauth polkit policies installation

* Thu Jan 07 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.3.90-3
- bump min polkit-qt version(s)

* Wed Jan 06 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.3.90-2
- -devel: Requires: shared-desktop-ontologies-devel

* Wed Jan 06 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.3.90-1
- 4.3.90 (4.4rc1)
- drop openssl patch (no longer needed since bug #429846 fixed)

* Tue Jan 05 2010 Jaroslav Reznik <jreznik@redhat.com> - 4.3.85-7
- PolkitQt rebuild

* Sun Dec 27 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.85-6
- Conflicts: kdebase-workspace(-libs,-devel) < 4.3.80

* Sat Dec 26 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.85-5
- move kdecmake,makekdewidgets manpages to -devel (#549947)

* Sat Dec 19 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.85-4
- tarball respin

* Fri Dec 18 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.85-3
- -devel: Requires: attica-devel

* Fri Dec 18 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.85-2
- plasma_scrollwidget patch

* Fri Dec 18 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.85-1
- 4.3.85 (4.4 beta2)

* Wed Dec 16 2009 Jaroslav Reznik <jreznik@redhat.com> - 4.3.80-5
- Repositioning the KDE Brand (#547361)

* Wed Dec 09 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.80-4
- BR: attica-devel shared-desktop-ontologies-devel
- phonon_ver 4.3.80
- soprano_ver 2.3.70

* Fri Dec 04 2009 Than Ngo <than@redhat.com> - 4.3.80-3
- respin

* Thu Dec 03 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.3.80-2
- BR polkit-qt-devel
- fix the build of the KAuth PolkitQt-1 backend (upstream patch)

* Tue Dec 01 2009 Ben Boeckel <MathStuf@gmail.com> - 4.3.80-1
- KDE 4.4 beta1 (4.3.80)

* Wed Nov 25 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.75-0.2.svn1048496
- -devel: Provides: kdelibs4-devel%%{?_isa} ...
- Obsoletes: kdelibs-experimental(-devel) < 4.3.75

* Fri Nov 20 2009 Ben Boeckel <MathStuf@gmail.com> - 4.3.75-0.1.svn1048496
- Update to 4.3.75 snapshot

* Wed Nov 18 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.3-6
- rebuild (for qt-4.6.0-rc1, f13+)
- fix/revert soprano_ver change in -5

* Mon Nov 16 2009 Than Ngo <than@redhat.com> - 4.3.3-5
- fix conditional

* Fri Nov 13 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.3-4
- kubuntu_80_kaction_qt_keys.diff (#475247)
- soprano_ver 2.3.1

* Fri Nov 13 2009 Than Ngo <than@redhat.com> - 4.3.3-3
- rhel cleanup, fix conditional for RHEL

* Fri Nov 06 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.3.3-2
- backport adFilteredBy API from trunk, required to build konq-plugins-4.3.3
- BR flex and bison for the Solid predicate parser
- fix build of fakes.c due to missing #include <string.h>

* Fri Oct 30 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.3-1
- 4.3.3

* Mon Oct 12 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.3.2-4
- khtml kpart crasher nr. 2 (rev.1033984)

* Thu Oct 08 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.2-3
- khtml kpart crasher (kde #207173/209876)

* Wed Oct 07 2009 Than Ngo <than@redhat.com> - 4.3.2-2
- fix a deadlock in KLocale

* Mon Oct 05 2009 Than Ngo <than@redhat.com> - 4.3.2-1
- 4.3.2

* Wed Sep 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.1-7
- move /etc/profile.d/kde4.(sh|csh) to kde-settings (F-12+)

* Mon Sep 21 2009 Than Ngo <than@redhat.com> - 4.3.1-6
- use abrt for RHEL

* Sat Sep 19 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.1-5
- groupdav connect to egroupware failed (kde#186763)

* Fri Sep 18 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.3.1-4
- ship kde4-doxygen.sh only in -devel (fix duplicate file)

* Fri Sep 04 2009 Than Ngo <than@redhat.com> - 4.3.1-3
- security fix for -CVE-2009-2702

* Wed Sep 02 2009 Ben Boeckel <MathStuf@gmail.com> - 4.3.1-2
- Patch for kde#160679

* Fri Aug 28 2009 Than Ngo <than@redhat.com> - 4.3.1-1
- 4.3.1
- openssl-1.0 build fixes

* Wed Aug 26 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.0-8
- BR: xz-devel

* Sun Aug 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.0-7
- buildsys_phonon patch (to be compatible with newer kde-qt.git qt builds)

* Wed Aug 19 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.3.0-6
- fix crash when editting toolbars (kdebug:200815)

* Tue Aug 18 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.3.0.5
- fix KDE bug #19538, copy file after rename uses old file name

* Mon Aug 17 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.3.0-4
- fix unmounting devices
- fix copying URLs to clipboard (kdebug:170608)

* Fri Aug 14 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.0-3
- kde4.(sh|csh): drop KDE_IS_PRELINKED for now (workaround bug #515539)

* Wed Aug 05 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.0-2
- microblog crashes plasma on show friends toggle (kdebug#202550)
- khtml crasher (kdebug#199557)

* Thu Jul 30 2009 Than Ngo <than@redhat.com> - 4.3.0-1
- 4.3.0

* Wed Jul 29 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.98-4
- -devel: Conflicts: kdebase-runtime < 4.2.90, kdebase-workspace-devel < 4.2.90

* Sun Jul 26 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.2.98-3
- fix CVE-2009-2537 - select length DoS
- fix CVE-2009-1725 - crash, possible ACE in numeric character references
- fix CVE-2009-1687 - possible ACE in KJS (FIXME: now aborts, so still crashes)
- fix CVE-2009-1698 - crash, possible ACE in CSS style attribute handling
- fix minimum strigi version (0.7, not 0.7.0, RPM thinks 0.7 < 0.7.0)

* Fri Jul 24 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.98-2
- respun tarball, to fix KIO HTTP redirects
- fix phonon/strigi versions

* Wed Jul 22 2009 Than Ngo <than@redhat.com> - 4.2.98-1
- 4.3rc3

* Thu Jul 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.96-2
- soprano_ver 2.3.0
- License: LGPLv2+

* Fri Jul 10 2009 Than Ngo <than@redhat.com> - 4.2.96-1
- 4.3rc2

* Wed Jul 08 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.2.95-4
- fix CMake dependency in parallel_devel patch (#510259, CHIKAMA Masaki)

* Fri Jul 03 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.95-3
- plasma animation crasher (kdebug#198338)

* Fri Jul 03 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.95-2
- up min versions, phonon, strigi, soprano (#509511)

* Thu Jun 25 2009 Than Ngo <than@redhat.com> - 4.2.95-1
- 4.3 rc1

* Wed Jun 03 2009 Rex Dieter <rdieter@fedoraproject.org> 4.2.90-1
- KDE-4.3 beta2 (4.2.90)

* Tue May 12 2009 Than Ngo <than@redhat.com> 4.2.85-1
- KDE-4.3 beta1 (4.2.85)
- kde4.(sh|csh): drop QT_PLUGINS_PATH munging, kde4-config call (#498809)

* Wed Apr 29 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.2-14
- -devel: Provides: kdelibs4-devel%%{?_isa} ...

* Tue Apr 28 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.2-13
- upstream patch to fix GCC4.4 crashes in kjs
  (kdebug:189809)

* Fri Apr 24 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.2.2-12
- drop the PopupApplet configuration backports (#495998) for now, kconf_update
  does not work as expected for Plasma

* Thu Apr 23 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.2.2-11
- fix the kconf_update scriptlet for #495998 again (missing DELETEGROUP)

* Thu Apr 23 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.2.2-10
- fix the kconf_update scriptlet for #495998 (broken .upd syntax)

* Tue Apr 21 2009 Than Ngo <than@redhat.com> - 4.2.2-9
- don't let plasma appear over screensaver

* Mon Apr 20 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.2.2-8
- fix Plasma PopupApplet configuration interfering with weather applet (#495998)

* Sun Apr 19 2009 Rex Dieter <rdieter@fedoraproject.org> 4.2.2-7
- fix and simplify the child struct disposal (kde#180785)

* Sat Apr 18 2009 Rex Dieter <rdieter@fedoraproject.org> 4.2.2-6
- squash leaky file descriptors in kdeinit (kde#180785,rhbz#484370)

* Fri Apr 10 2009 Rex Dieter <rdieter@fedoraproject.org> 4.2.2-5
- fix bidi-related hangs in khtml (kde#189161)

* Wed Apr 08 2009 Than Ngo <than@redhat.com> - 4.2.2-4
- upstream patch fix ReadOnlyPart crash for non-local file

* Tue Apr 07 2009 Than Ngo <than@redhat.com> - 4.2.2-3
- fix kickoff focus issue

* Tue Apr 07 2009 Than Ngo <than@redhat.com> - 4.2.2-2
- upstream patch to fix kio_http issue

* Wed Apr  1 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.2-1
- KDE 4.2.2

* Mon Mar 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.1-9
- scriptlet optimization

* Thu Mar 19 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.1-8
- Provides: kdelibs4%%{?_isa} ... (#491082)

* Wed Mar 18 2009 Rex Dieter <rdieter@fedoraproject.org> 4.2.1-7
- Provides: kross(javascript) kross(qtscript)  (#490586)

* Thu Mar 12 2009 Than Ngo <than@redhat.com> - 4.2.1-6
- apply patch to fix encoding for Qt-4.5.0

* Mon Mar 09 2009 Than Ngo <than@redhat.com> - 4.2.1-5
- apply patch to fix issue in CSS style that causes konqueror shows a blank page

* Thu Mar 05 2009 Rex Dieter <rdieter@fedorproject.org> - 4.2.1-4
- move designer plugins to main/runtime (#487622)

* Sun Mar 01 2009 Than Ngo <than@redhat.com> - 4.2.1-2
- respin

* Fri Feb 27 2009 Than Ngo <than@redhat.com> - 4.2.1-1
- 4.2.1

* Thu Feb 26 2009 Than Ngo <than@redhat.com> 4.2.0-17
- fix build issue against gcc44

* Wed Feb 25 2009 Than Ngo <than@redhat.com> - 4.2.0-16
- fix files conflicts with 3.5.x

* Tue Feb 24 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.2.0-15
- fix crash in ~KMainWindow triggered by sending messages in KNode (kde#182322)

* Mon Feb 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.0-14
- (Build)Req: soprano(-devel) >= 2.2
- devel: drop Req: zlib-devel libutempter-devel

* Wed Feb 18 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.2.0-13
- disable strict aliasing in kjs/dtoa.cpp (GCC 4.4 x86_64 crash) (#485968)

* Thu Feb 12 2009 Than Ngo <than@redhat.com> - 4.2.0-11
- make plasma work better with Qt 4.5 (when built against Qt 4.5)
- add gcc44-workaround

* Fri Feb 06 2009 Than Ngo <than@redhat.com> - 4.2.0-10
- Fix duplicated applications in the K menu and in keditfiletype

* Thu Feb 05 2009 Rex Dieter <rdieter@fedoraproject.org> 4.2.0-9
- ssl/proxy patch (kde#179934)

* Sat Jan 31 2009 Rex Dieter <rdieter@fedoraproject.org> 4.2.0-8
- unowned dirs (#483315,#483318)

* Fri Jan 30 2009 Rex Dieter <rdieter@fedoraproject.org> 4.2.0-7
- kded/kdirwatch patch (kde#182472)

* Fri Jan 30 2009 Lukáš Tinkl <ltinkl@redhat.com> 4.2.0-6
- Emit the correct FilesRemoved signal if the job was aborted in the middle of its operation,
  otherwise it can result in confusion and data loss (overwriting files with files
  that don't exist). kdebug:118593
- Fix "klauncher hangs when kdeinit4 dies" -- this happened because
  klauncher was doing a blocking read forever.
- Repair klauncher support for unique-applications like konsole.
  kdebug:162729, kdebug:75492

* Fri Jan 30 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.2.0-5
- reenable PolicyKit and NTFS workarounds

* Mon Jan 26 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.0-4
- revert Requires: qt4%%{_isa}

* Mon Jan 26 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.0-3
- respun tarball

* Mon Jan 26 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.0-2
- plasma-on-screensaver-security patch
- (Build)Req: automoc4 >= 0.9.88, phonon(-devel) >= 4.3.0
- Requires: strigi-libs >= 0.6.3
- use %%{?_isa} to avoid potential multilib heartbreak

* Thu Jan 22 2009 Than Ngo <than@redhat.com> - 4.2.0-1
- 4.2.0

* Fri Jan 16 2009 Than Ngo <than@redhat.com> - 4.1.96-9
- drop kdelibs-4.1.85-plasma-default-wallpaper.patch, it's not needed
  since new plasma allows to define default wallpaper, new kde-setting
  is required
- backport fix from trunk to allow symlinks in wallpaper theme

* Fri Jan 16 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.1.96-8
- rebuild for new OpenSSL

* Mon Jan 12 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.1.96-7
- Slight speedup to profile.d/kde.sh (#465370)
- (Build)Req: strigi(-devel) >= 0.6.3

* Mon Jan 12 2009 Than Ngo <than@redhat.com> - 4.1.96-6
- fix a crash (appearing in KSMServer)

* Sat Jan 10 2009 Than Ngo <than@redhat.com> - 4.1.96-5
- kdeworkspace cmake files in correct place

* Fri Jan 09 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.1.96-4
- bump min deps (cmake, kde-filesystem, phonon)
- kde.(sh|csh): cleanup QT_PLUGIN_PATH handling (#477095)
- Requires: coreutils grep

* Fri Jan 09 2009 Than Ngo <than@redhat.com> - 4.1.96-3
- BR soprano >= 2.1.64

* Thu Jan 08 2009 Than Ngo <than@redhat.com> - 4.1.96-2
- kdepim cmake files in correct place

* Wed Jan 07 2009 Than Ngo <than@redhat.com> - 4.1.96-1
- 4.2rc1

* Fri Dec 19 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.85-6
- add plasma-default-wallpaper libplasma patch from kdebase-workspace-4.1

* Tue Dec 16 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.85-5
- respun tarball, integrates kde-l10n-systemsettings patch

* Tue Dec 16 2008 Than Ngo <than@redhat.com> - 4.1.85-4
- add missing ENTITY systemsettings in pt, that fixes kde-l10
  build breakage

* Mon Dec 15 2008 Than Ngo <than@redhat.com> - 4.1.85-3
- add missing ENTITY systemsettings in ru/gl/es/pt, that fixes kde-l10
  build breakage
- rename suffix .xxcmake to avoid install .cmake

* Sun Dec 14 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.1.85-2
- tweak parallel_devel patch to get a -L flag for the symlink directory

* Thu Dec 11 2008 Than Ngo <than@redhat.com> -  4.1.85-1
- 4.2beta2

* Tue Dec 09 2008 Lorenzo Villani <lvillani@binaryhelix.net> - 6:4.1.82-2
- rebase parallel devel patch and kde149705 patch

* Mon Dec 08 2008 Lorenzo Villani <lvillani@binaryhelix.net> - 6:4.1.82-1
- 4.1.82

* Tue Nov 25 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.80-5
- remove workaround BR on phonon-backend-gstreamer, it's ineffective since
  phonon now explicitly Requires: phonon-backend-xine and the dependency is no
  longer circular anyway
- update parallel_devel patch
- fix minimum strigi version (only 0.5.9 needed)

* Tue Nov 25 2008 Than Ngo <than@redhat.com> 4.1.80-4
- respin

* Thu Nov 20 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.80-3
- -devel: Provides: plasma-devel

* Thu Nov 20 2008 Than Ngo <than@redhat.com> 4.1.80-2
- merged

* Thu Nov 20 2008 Lorenzo Villani <lvillani@binaryhelix.net> - 6:4.1.80-1
- 4.1.80
- BR strigi 0.60
- BR cmake 2.6
- make install/fast
- rebase policykit patch
- rebase cmake patch
- rebase a couple of patches and drop _default_patch_fuzz 2

* Wed Nov 12 2008 Than Ngo <than@redhat.com> 4.1.3-1
- 4.1.3

* Fri Nov 07 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.2-6
- backport http_cache_cleaner fix (kdebug:172182)

* Wed Oct 15 2008 Lukáš Tinkl <ltinkl@redhat.com> 4.1.2-5
- backport fix for faulty window resizing (kdebug:172042)

* Mon Oct 13 2008 Than Ngo <than@redhat.com> 4.1.2-4
- backport patch to fix crash kded startup crash

* Wed Oct 08 2008 Than Ngo <than@redhat.com> 4.1.2-3
- backport fix for google maps

* Sun Sep 28 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.2-2
- make VERBOSE=1
- respin against new(er) kde-filesystem

* Thu Sep 25 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.2-1
- kde-4.1.2

* Fri Sep 19 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.1-12
- make "Stop Animations" work again in Konqueror (KDE 4 regression kde#157789)

* Thu Sep 18 2008 Than Ngo <than@redhat.com> 4.1.1-11
- apply upstream patch to fix the regression
- drop the kdelibs-4.1.1-bz#461725-regression.patch

* Thu Sep 18 2008 Lukáš Tinkl <ltinkl@redhat.com> 4.1.1-10
- Fix file association bug, the global mimeapps.list file had priority
  over the local one.
- khtml scroll crash fix (kdebug:170880)
- Don't eat text when the emoticons were not installed. This fixes
  mail text not being displayed in KMail when kdebase-runtime wasn't
  installed.

* Wed Sep 17 2008 Than Ngo <than@redhat.com> 4.1.1-9
- #461725, revert the patch to fix the regression

* Sat Sep 13 2008 Than Ngo <than@redhat.com> 4.1.1-8
- fix kdelibs-4.1.1-kdeui-widgets-fixes.patch

* Sat Sep 13 2008 Than Ngo <than@redhat.com> 4.1.1-7
- remove redundant FEDORA, use CMAKE_BUILD_TYPE=release
- fix install problem with cmake > 2.5

* Mon Sep 08 2008 Lukáš Tinkl <ltinkl@redhat.com> 4.1.1-6
- fix crashes in plugin selector
- fix problems in various kdeui widgets

* Wed Sep 03 2008 Lukáš Tinkl <ltinkl@redhat.com> 4.1.1-5
- fixed crash on setting cookies on empty domains (like the file
  system), KDE bug #170147
- fix URL navigator focus in file dialogs, KDE bug #169497, #170211

* Tue Sep 02 2008 Than Ngo <than@redhat.com> 4.1.1-4
- apply patch to fix regression in khtml

* Mon Sep 01 2008 Than Ngo <than@redhat.com> 4.1.1-3
- respun

* Fri Aug 29 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.1-2
- fix #455130 (kinit crashing in kglobalconfig with no KComponentData) properly
- drop revert-kinit-regression hack (fixes ioslave translations)

* Fri Aug 29 2008 Than Ngo <than@redhat.com> 4.1.1-1
- 4.1.1

* Fri Aug 29 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.0-9
- -devel: +Requires: libutempter-devel (cmake wants to link it in)

* Thu Aug 28 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.0-8
- rewrite kstandarddirs patch to fix side effects (#459904 (KDEDIRS), #457633)

* Mon Aug 25 2008 Than Ngo <than@redhat.com> 4.1.0-7
- konsole doesn't write to utmp

* Sat Aug 23 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.0-6
- don't hide KDE 3 KCMs in kde4-applications.menu, not needed with our
  OnlyShowIn=KDE3 patch and breaks KDE 3 KCMs (kcmshell, apps) in KDE 4 sessions

* Sun Aug 10 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.0-5
- fix kcookiejar crash on invalid cookie file from KDE 3 (patch by David Faure)

* Fri Aug 01 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.0-4
- -devel: Requires: phonon-devel >= 4.2 (helps multilib upgrades)
- konq processes never terminate (kde#167826, rh#457526)

* Wed Jul 30 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.0-3
- (Build)Requires: soprano(-devel) >= 2.1 (#456827)

* Thu Jul 24 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.0-2
- move Sonnet documentation back to the main package
- fix #341751 (Sonnet documentation multilib conflict) properly

* Wed Jul 23 2008 Than Ngo <than@redhat.com> 4.1.0-1
- 4.1.0

* Sun Jul 20 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.99-3
- fix kstandarddirs patch to always append the installed location last, even if
  it is already present earlier in the search path (#456004)

* Sat Jul 19 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.99-2
- use better fedora-buildtype patch from F-9 branch

* Fri Jul 18 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.99-1
- 4.0.99

* Mon Jul 14 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.98-4
- respun tarball

* Sat Jul 12 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.0.98-2
- revert a kinit patch causing an assertion failure in KComponentData (#455130)

* Thu Jul 10 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.98-1
- 4.0.98
- omit proxy patch (fixed upstream)

* Sun Jul 06 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.85-1
- 4.0.85

* Fri Jun 27 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.84-1
- 4.0.84

* Fri Jun 27 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.0.83-3
- fix kstandarddirs patch so /usr/libexec/kde4 is found (#453063)

* Wed Jun 25 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.83-2
- -common: move %{_kde4_docdir}/HTML/en/sonnet/ here (#341751)

* Thu Jun 19 2008 Than Ngo <than@redhat.com> 4.0.83-1
- 4.0.83 (beta2)

* Fri Jun 13 2008 Than Ngo <than@redhat.com> 4.0.82-1
- 4.0.82

* Fri May 30 2008 Than Ngo <than@redhat.com> 4.0.80-2
- fix #447965, order issue in kde path, thanks to Kevin
- backport patch to check html style version

* Mon May 26 2008 Than Ngo <than@redhat.com> 4.0.80-1
- 4.1 beta1

* Sat May 24 2008 Rex Dieter <rdieter@fedoraproject.org> - 4.0.72-8
- revert previous, don't include kde3-compat symlink (here, anyway)

* Fri May 23 2008 Rex Dieter <rdieter@fedoraproejct.org> - 4.0.72-7
- -common: provide %%_datadir/apps/kdeui for kde3 apps (#447965)

* Thu May 22 2008 Rex Dieter <rdieter@fedoraproject.org> - 4.0.72-6
- kstandarddirs hack to search /etc/kde

* Thu May 22 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.0.72-5
- keep libphonon.so in %%{_libdir} for non-KDE apps (#447831)

* Thu May 15 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.0.72-4
- fix proxy support (#443931, kde#155707)
- move %%{_kde4_appsdir}/ksgmltools2/ from -devel to the main package (#446435)

* Tue May 13 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.0.72-3
- drop no longer needed ALSA default device Phonon hack

* Sun May  4 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.0.72-2
- BR new minimum versions of qt4-devel and soprano-devel

* Fri May  2 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.0.72-1
- update to 4.0.72 (4.1 alpha 1)
- parallel_devel patch ported by Lorenzo Villani <lvillani@binaryhelix.net>
- update file list (Lorenzo Villani)
- drop upstreamed khtml-security, kconfig_sync_crash and klauncher-crash patches
- update xdg-menu (Administration menu) patch

* Tue Apr 22 2008 Lukáš Tinkl <ltinkl@redhat.com> - 4.0.3-7
- fix buffer overflow in KHTML's image loader (KDE advisory 20080426-1,
  #443766: CVE-2008-1670)

* Fri Apr 04 2008 Than Ngo <than@redhat.com> -  4.0.3-6
- apply upstream patch to fix klauncher crash
- fix kconfig_sync_crash patch

* Fri Apr  4 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.3-5
- kconfig_sync_crash patch

* Thu Apr  3 2008 Lukáš Tinkl <ltinkl@redhat.com> 4.0.3-4
- rebuild for the new %%{_kde4_buildtype}

* Mon Mar 31 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.3-3
- patch and update file list for _kde4_libexecdir

* Mon Mar 31 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.3-2
- add Fedora build type (uses -DNDEBUG)

* Fri Mar 28 2008 Than Ngo <than@redhat.com> 4.0.3-1
- 4.0.3
- -apidocs: drop Requires: %%name

* Fri Mar 28 2008 Than Ngo <than@redhat.com> -  4.0.2-13
- add Administration menu, bz#439378

* Thu Mar 27 2008 Than Ngo <than@redhat.com> 4.0.2-12
- bz#428212, adapted Kevin Kofler's workaround for Policykit

* Thu Mar 20 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.2-11
- apidocs subpackage should be noarch (#436579)

* Mon Mar 10 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.2-10
- work around #436725: BR: libtool-ltdl so graphviz gets a valid libltdl

* Mon Mar 10 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.2-9
- fix kdeglobals not being found in profile (e.g. kde-settings) directory

* Fri Mar 07 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.2-8
- touchup KDE_DISTRIBUTION_TEXT
- add Fedora/V-R to KHTML UA string (thanks caillon)

* Thu Mar 06 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.2-7
- exclude apidocs from the main package

* Thu Mar 06 2008 Than Ngo <than@redhat.com> 4.0.2-6
- apply upstream patch to fix issue in KPropertiesDialog

* Thu Mar 06 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.2-5
- also install Doxyfile.global in -common to build kdepimlibs-apidocs against

* Wed Mar 05 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.2-4
- install all .css files in kdelibs-common to build kdepimlibs-apidocs against
- install doxygen.sh as kde4-doxygen.sh in -devel
- build apidocs and put them into an -apidocs subpackage (can be turned off)
- BR doxygen, graphviz and qt4-doc when building apidocs

* Fri Feb 29 2008 Than Ngo <than@redhat.com> 4.0.2-3
- rebuilt

* Fri Feb 29 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.2-2
- drop obsolete kde#149703 patch (fixed upstream by code rewrite)
- drop backports from 4.0.2: objectembed-handling, autostart, kde#771201-khtml

* Thu Feb 28 2008 Than Ngo <than@redhat.com> 4.0.2-1
- 4.0.2

* Wed Feb 27 2008 Lukáš Tinkl <ltinkl@redhat.com> - 4.0.1-8
- add Fedora branding to the package (#434815)

* Mon Feb 25 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.1-7
- -devel: own %%_kde4_libdir/kde4/plugins (thanks wolfy!)

* Tue Feb 19 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.1-6
- fix running KDE 3 apps as filetype viewers from KDE 4 Dolphin

* Mon Feb 18 2008 Rex Dieter <rdieter@fedoraprojectorg> 4.0.1-5
- -devel: include %%_kde4_appsdir/cmake here (#341751)

* Wed Feb 06 2008 Than Ngo <than@redhat.com> 4.0.1-4
- upstream patch to make sure that static widget is always at position 0,0

* Fri Feb 01 2008 Than Ngo <than@redhat.com> 4.0.1-3
- upstream patch to fix a regression in <object><embed> handling
- autostart upstream patch

* Fri Feb 01 2008 Than Ngo <than@redhat.com> 4.0.1-2
- autostart from XDG_CONFIG_DIRS

* Wed Jan 30 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.1-1
- 4.0.1

* Wed Jan 30 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.0-4
- omit openssl patch (f9+ #429846)
- respin (qt4)

* Wed Jan 23 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.0-3
- openssl patch

* Sat Jan 19 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.0-2
- patch K3Spell for hunspell support on F9+ (FeatureDictionary, kde#154561)

* Mon Jan 07 2008 Than Ngo <than@redhat.com> 4.0.0-1
- 4.0.0
