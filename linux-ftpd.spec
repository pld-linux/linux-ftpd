Summary:	FTP Daemon
Summary(pl):	Serwer FTP
Name:		linux-ftpd
Version:	0.17
Release:	1
License:	BSD
Group:		Daemons
Group(de):	Server
Group(pl):	Serwery
Source0:	ftp://ftp.linux.org.uk/pub/linux/Networking/netkit/%{name}-%{version}.tar.gz
Source1:	%{name}.inetd
Prereq:		rc-inetd
Requires:	inetdaemon
Provides:	ftpserver
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	ftpserver
Obsoletes:	anonftp
Obsoletes:	bftpd
Obsoletes:	ftpd-BSD
Obsoletes:	heimdal-ftpd
Obsoletes:	muddleftpd
Obsoletes:	proftpd
Obsoletes:	pure-ftpd
Obsoletes:	troll-ftpd
Obsoletes:	wu-ftpd

%define		_sysconfdir	/etc
%define		_homedir	/home/ftp/pub

%description
The linux-ftpd package contains the linux-ftpd FTP (File Transfer
Protocol) server daemon.  The FTP protocol is a method of transferring
files between machines on a network and/or over the Internet. 
Supports shadowed passowrds. Does not (yet) support PAM.

%description -l pl
Ten pakiet zawiera serwer FTP (protoko³u transmisji plików)
linux-ftpd. Protokó³ FTP jest sposobem transmisji plików pomiêdzy
maszynami w sieci i przez Internet. linux-ftpd obs³uguje has³a w pliku
shadow, na razie nie wspiera PAM.

%prep
%setup -q

%build
./configure \
	--installroot=$RPM_BUILD_ROOT \
	--prefix=%{_prefix}

%{__make} CFLAGS="%{rpmcflags} -I../support"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man{5,8}}
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_homedir}/Incoming}
install -d $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd

%{__make} install INSTALLROOT=$RPM_BUILD_ROOT \
	SBINDIR=%{_sbindir} \
	MANDIR=%{_mandir} \
	DAEMONMODE=755 \
	MANMODE=644 

rm -f $RPM_BUILD_ROOT%{_sbindir}/in.ftpd
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/rc-inetd/ftpd

:> $RPM_BUILD_ROOT%{_sysconfdir}/ftpusers.default
:> $RPM_BUILD_ROOT%{_sysconfdir}/ftpusers

mv -f ftpd/ftpd $RPM_BUILD_ROOT%{_sbindir}/ftpd

gzip -9nf README ChangeLog

%clean
rm -rf $RPM_BUILD_ROOT

%post 
awk 'BEGIN { FS = ":" }; { if($3 < 1000) print $1; }' < /etc/passwd >> %{_sysconfdir}/ftpusers.default
if [ ! -f %{_sysconfdir}/ftpusers ]; then
	( cd %{_sysconfdir}; mv -f ftpusers.default ftpusers )
fi

if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun
if [ "$1" = "0" -a -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
fi

%files
%defattr(644,root,root,755)
%doc {ChangeLog,README}.gz

%attr(755,root,root) %dir %{_sysconfdir}

%attr(640,root,root) %{_sysconfdir}/ftpusers.default
%attr(640,root,root) %ghost %{_sysconfdir}/ftpusers
%attr(640,root,root) /etc/sysconfig/rc-inetd/ftpd

%attr(755,root,root) %{_sbindir}/ftpd
%{_mandir}/man[58]/*

%dir /home/ftp/pub
%attr(711,root,root) %dir /home/ftp/pub/Incoming
