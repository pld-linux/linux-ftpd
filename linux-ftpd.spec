Summary:	FTP Daemon
Summary(pl.UTF-8):	Serwer FTP
Name:		linux-ftpd
Version:	0.17
Release:	3
License:	BSD
Group:		Daemons
Source0:	ftp://ftp.linux.org.uk/pub/linux/Networking/netkit/%{name}-%{version}.tar.gz
# Source0-md5:	f5f491564812db5d8783daa538c49186
Source1:	%{name}.inetd
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post):	awk
Requires(post):	fileutils
Requires:	inetdaemon
Requires:	rc-inetd
Provides:	ftpserver
Obsoletes:	anonftp
Obsoletes:	bftpd
Obsoletes:	ftpd-BSD
Obsoletes:	ftpserver
Obsoletes:	glftpd
Obsoletes:	heimdal-ftpd
Obsoletes:	muddleftpd
Obsoletes:	proftpd
Obsoletes:	proftpd-common
Obsoletes:	proftpd-inetd
Obsoletes:	proftpd-standalone
Obsoletes:	pure-ftpd
Obsoletes:	troll-ftpd
Obsoletes:	vsftpd
Obsoletes:	wu-ftpd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_homedir	/home/services/ftp/pub

%description
The linux-ftpd package contains the linux-ftpd FTP (File Transfer
Protocol) server daemon. The FTP protocol is a method of transferring
files between machines on a network and/or over the Internet. Supports
shadowed passowrds. Does not (yet) support PAM.

%description -l pl.UTF-8
Ten pakiet zawiera serwer FTP (protokołu transmisji plików)
linux-ftpd. Protokół FTP jest sposobem transmisji plików pomiędzy
maszynami w sieci i przez Internet. linux-ftpd obsługuje hasła w pliku
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

%{__make} install \
	INSTALLROOT=$RPM_BUILD_ROOT \
	SBINDIR=%{_sbindir} \
	MANDIR=%{_mandir} \
	DAEMONMODE=755 \
	MANMODE=644

rm -f $RPM_BUILD_ROOT%{_sbindir}/in.ftpd
install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/ftpd

:> $RPM_BUILD_ROOT%{_sysconfdir}/ftpusers.default
:> $RPM_BUILD_ROOT%{_sysconfdir}/ftpusers

mv -f ftpd/ftpd $RPM_BUILD_ROOT%{_sbindir}/ftpd

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 027
awk 'BEGIN { FS = ":" }; { if($3 < 500) print $1; }' < /etc/passwd >> %{_sysconfdir}/ftpusers.default
if [ ! -f %{_sysconfdir}/ftpusers ]; then
	( cd %{_sysconfdir}; mv -f ftpusers.default ftpusers )
fi

%service -q rc-inetd reload

%postun
if [ "$1" = "0" ]; then
	%service -q rc-inetd reload
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog README

%attr(640,root,root) %config(missingok) %verify(not md5 mtime size) %{_sysconfdir}/ftpusers.default
%attr(640,root,root) %ghost %{_sysconfdir}/ftpusers
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/ftpd

%attr(755,root,root) %{_sbindir}/ftpd
%{_mandir}/man[58]/*

%dir /home/services/ftp/pub
%attr(711,root,root) %dir /home/services/ftp/pub/Incoming
