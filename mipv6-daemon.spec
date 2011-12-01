Name:		mipv6-daemon
Version:	0.4
Release:	5%{?dist}
Summary:	Mobile IPv6 (MIPv6) Daemon

Group:		System Environment/Daemons
License:	GPLv2
URL:		http://www.linux-ipv6.org/memo/mipv6/
Source0:	ftp://ftp.linux-ipv6.org/pub/usagi/patch/mipv6/umip-%{version}/daemon/tarball/mipv6-daemon-umip-%{version}.tar.gz
Source1:	mip6d.init
Source2:	mip6d.sysconfig
Source3:	mip6d.conf
Patch0:		mipv6-daemon-header-fix.patch
Patch1:		mipv6-daemon-nemo.patch
Patch2:		mipv6-daemon-netlink-msg-origin-check.patch
Patch3:		mipv6-daemon-nd-opts-sanity-check.patch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	flex bison indent
Requires:	initscripts, chkconfig

%description
The mobile IPv6 daemon allows nodes to remain
reachable while moving around in the IPv6 Internet.

%prep
%setup -q -n mipv6-daemon-umip-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_initrddir}
install -m755 %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/mip6d
install -d $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/mip6d
install -m644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/mip6d.conf

%clean
rm -rf $RPM_BUILD_ROOT

%preun
if [ "$1" = 0 ]
then
	/sbin/service mip6d stop > /dev/null 2>&1 ||:
	/sbin/chkconfig --del mip6d
fi

%post
/sbin/chkconfig --add mip6d

%postun
if [ "$1" -ge "1" ]; then
	/sbin/service mip6d condrestart > /dev/null 2>&1 ||:
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS BUGS COPYING NEWS README README.IPsec THANKS extras
%{_initrddir}/mip6d
%config(noreplace) %{_sysconfdir}/sysconfig/mip6d
%config(noreplace) %{_sysconfdir}/mip6d.conf
%{_sbindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*

%changelog
* Thu Jul 15 2010 Thomas Graf <tgraf at, redhat.com> 0.4-5
- Fix CVE-2010-2522 and CVE-2010-2523 by including the patches:
  - Additional sanity checks for ND options length
  - Security fix: Check origin of netlink messages in netlink helpers.
* Mon Jul 5 2010 Thomas Graf <tgraf at, redhat.com> 0.4-4
- Fixed initscript according to SysVInitScript guidelines:
    - Corrected usage text
    - Added force-reload, condrestart and try-restart actions
    - Fixed return code of status action
    - Only start/stop daemon if not already running/stopped
* Thu May 20 2010 Thomas Graf <tgraf at, redhat.com> 0.4-3
- Inclusion of NEPL patch (NEMO support)
* Tue Aug 17 2009 Thomas Graf <tgraf at, redhat.com> 0.4-1
- initial package release
