Name:		fprobe-ulog
Version:	1.1.1
Release:	1
Summary:	fprobe-ulog: a NetFlow probe
Group:		Network/Monitoring
License:	GPL
URL:		http://fprobe.sourceforge.net
Source0:	%{name}-%{version}.tar.bz2
Buildroot:	%{_tmppath}/%{name}-buildroot
Provides:	fprobe-ulog

%description
fprobe-ulog - libipulog-based tool that collect network traffic data and emit
it as NetFlow flows towards the specified collector. PlanetLab vesion.

%prep
%setup -q

%build
./configure --sbindir=/sbin --mandir=%{_mandir} --enable-uptime_trick=no $EXTRA_OPTIONS
make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
install -d -v %{buildroot}/etc/init.d
install -m 755 -v fprobe-initscript %{buildroot}/etc/init.d/fprobe-ulog
gzip --best %{buildroot}%{_mandir}/man8/fprobe-ulog.8

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README COPYING TODO
/etc/init.d/fprobe-ulog
/sbin/fprobe-ulog
%{_mandir}/man8/fprobe-ulog.8.gz

%post
chkconfig --add fprobe-ulog
chkconfig fprobe-ulog on
if [ "$PL_BOOTCD" != "1" ] ; then
	service fprobe-ulog start
    fi

%preun
# 0 = erase, 1 = upgrade
if [ "$1" -eq 0 ]; then
    if [ "$PL_BOOTCD" != "1" ] ; then
	service fprobe-ulog stop
    fi
    chkconfig fprobe-ulog off
    chkconfig --del fprobe-ulog
fi


%changelog
