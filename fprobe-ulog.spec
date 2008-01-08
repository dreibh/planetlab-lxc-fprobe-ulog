#
# $Id$
#
%define url $URL$

%define name fprobe-ulog
%define version 1.1.1
%define taglevel 1

%define release %{taglevel}%{?pldistro:.%{pldistro}}%{?date:.%{date}}

Summary:	fprobe-ulog: a NetFlow probe
Name: %{name}
Version: %{version}
Release: %{release}
Group:		Network/Monitoring
License:	GPL
#URL:		http://fprobe.sourceforge.net
Source0:	%{name}-%{version}.tar.bz2
Buildroot:	%{_tmppath}/%{name}-buildroot
Provides:	fprobe-ulog

Vendor: PlanetLab
Packager: PlanetLab Central <support@planet-lab.org>
Distribution: PlanetLab %{plrelease}
URL: %(echo %{url} | cut -d ' ' -f 2)

%description
fprobe-ulog - libipulog-based tool that collect network traffic data and emit
it as NetFlow flows towards the specified collector.

%prep
%setup -q

%build
./configure --sbindir=%{_sbindir} --mandir=%{_mandir} --enable-uptime_trick=no $EXTRA_OPTIONS
make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
gzip --best %{buildroot}%{_mandir}/man8/fprobe-ulog.8

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README COPYING TODO
/*
