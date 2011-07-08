#
# $Id$
#
%define url $URL$

# please keep these three lines as they are used by the tagging script
# see build/module-tag.py for details
%define name fprobe-ulog
%define version 1.1.3
%define taglevel 3

%define release %{taglevel}%{?pldistro:.%{pldistro}}%{?date:.%{date}}

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	fprobe-ulog: a NetFlow probe
Group:		Network/Monitoring
License:	GPL
#URL:		http://fprobe.sourceforge.net
URL: %(echo %{url} | cut -d ' ' -f 2)
Source0:	%{name}-%{version}.tar.bz2
Buildroot:	%{_tmppath}/%{name}-buildroot
Provides:	fprobe-ulog

%description
fprobe-ulog - libipulog-based tool that collect network traffic data and emit
it as NetFlow flows towards the specified collector. PlanetLab version.

%prep
%setup -q

%build
./configure --sbindir=/sbin --mandir=%{_mandir} --enable-uptime_trick=no $EXTRA_OPTIONS
make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
install -d -v %{buildroot}/etc/init.d
mkdir -p %{buildroot}/var/local/fprobe
install -m 755 -v fprobe-initscript %{buildroot}/etc/init.d/fprobe-ulog
gzip --best %{buildroot}%{_mandir}/man8/fprobe-ulog.8

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README COPYING TODO
/etc/init.d/fprobe-ulog
/sbin/fprobe-ulog
/var/local/fprobe
%{_mandir}/man8/fprobe-ulog.8.gz

%post
chkconfig --add fprobe-ulog
if [ "$PL_BOOTCD" != "1" ] ; then
    service fprobe-ulog condrestart
fi

%preun
# 0 = erase, 1 = upgrade
if [ "$1" -eq 0 ]; then
    if [ "$PL_BOOTCD" != "1" ] ; then
	service fprobe-ulog stop
    fi
    chkconfig --del fprobe-ulog
fi


%changelog
* Fri Jul 08 2011 Sapan Bhatia <sapanb@cs.princeton.edu> - fprobe-ulog-1.1.3-3
- This changeset makes fprobe compress the data it collects.

* Mon Apr 26 2010 Sapan Bhatia <sapanb@cs.princeton.edu> - fprobe-ulog-1.1.3-2
- This version uses the new location of the slice id field in /etc/vservers/vserver_name/<slice_id>. Needs Node Manager
- 2.0-6 and higher to function.

* Fri Nov 06 2009 Daniel Hokka Zakrisson <daniel@hozac.com> - fprobe-ulog-1.1.3-1
- Proper initscript semantics.

* Sun Sep 14 2008 Sapan Bhatia <sapanb@cs.princeton.edu> - fprobe-ulog-1.1.2-6
- Codemux support: react to changes in the xid of a connection to update the corresponding flow record.

* Wed Sep 10 2008 Sapan Bhatia <sapanb@cs.princeton.edu> - fprobe-ulog-1.1.2-5
- Bug fix, although not major.

* Tue Jul 01 2008 Sapan Bhatia <sapanb@cs.princeton.edu> - fprobe-ulog-1.1.2-4
- This change is required for PlanetFlow data collection on PLE. It makes fprobe data accessible to non-root users such
- as pl[e]_netflow.

* Mon May 05 2008 Stephen Soltesz <soltesz@cs.princeton.edu> - fprobe-ulog-1.1.2-3
- 


%define module_current_branch 1.1.2
