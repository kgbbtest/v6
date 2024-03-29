# Copyright (c) 2010, 2011, The Trusted Domain Project.  All rights reserved.
#

Summary: An open source library and milter for providing DKIM service
Name: opendkim
Version: 2.10.3
Release: 1
License: BSD
Group: System Environment/Daemons
Requires: libopendkim = %{version}-%{release}
BuildRequires: sendmail-devel, openssl-devel


Source: opendkim-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Prefix: %{_prefix}

%description
The Trusted Domain Project is a community effort to develop and maintain a
C library for producing DKIM-aware applications and an open source milter for
providing DKIM service through milter-enabled MTAs.

%package -n libopendkim
Summary: An open source DKIM library
Group: System Environment/Libraries

%description -n libopendkim
This package contains the library files required for running services built
using libopendkim.

%package -n libopendkim-devel
Summary: Development files for libopendkim
Group: Development/Libraries
Requires: libopendkim

%description -n libopendkim-devel
This package contains the static libraries, headers, and other support files
required for developing applications against libopendkim.

%prep
%setup

%build
# Required for proper OpenSSL support on some versions of RedHat
if [ -d /usr/include/kerberos ]; then
	INCLUDES="$INCLUDES -I/usr/include/kerberos"
fi
./configure --prefix=%{_prefix} --sysconfdir=%{_sysconfdir} --libdir=%{_libdir} --mandir=%{_mandir}  CPPFLAGS="$INCLUDES"

make

%install
make install DESTDIR="$RPM_BUILD_ROOT"
mkdir -p "$RPM_BUILD_ROOT"%{_sysconfdir}
mkdir -p "$RPM_BUILD_ROOT"%{_initrddir}
install -m 0755 contrib/init/generic/opendkim "$RPM_BUILD_ROOT"%{_initrddir}/%{name}
echo '## Basic OpenDKIM config file for verification only
## See opendkim.conf(5) or %{_docdir}/%{name}-%{version}/opendkim.conf.sample for more
PidFile %{_localstatedir}/run/opendkim/opendkim.pid
Mode	v
Syslog	yes
#Umask   002
#UserID  opendkim:mail
#Socket	local:%{_localstatedir}/run/opendkim/opendkim.socket
Socket  inet:8891@localhost

## After setting Mode to "sv", running
## opendkim-genkey -D %{_sysconfdir}/opendkim -s key -d `hostname --domain`
## and putting %{_sysconfdir}/opendkim
#Canonicalization        relaxed/simple
#Domain                  example.com # change to domain
#Selector                key
#KeyFile                 %{_sysconfdir}/opendkim/key.private
' > "$RPM_BUILD_ROOT"%{_sysconfdir}/opendkim.conf
rm -r "$RPM_BUILD_ROOT"%{_prefix}/share/doc/opendkim

%post
if ! getent passwd opendkim >/dev/null 2>&1; then
	%{_sbindir}/useradd -M -d %{_localstatedir}/lib -r -s /bin/false opendkim
	if ! getent group opendkim >/dev/null; then
		%{_sbindir}/groupadd opendkim
		%{_sbindir}/usermod -g opendkim opendkim
	fi
	if getent group mail >/dev/null; then
		%{_sbindir}/usermod -G mail opendkim
	fi
fi
test -d %{_localstatedir}/run/opendkim || mkdir %{_localstatedir}/run/opendkim
chown opendkim:opendkim %{_localstatedir}/run/opendkim
if [ ! -d %{_sysconfdir}/opendkim ]; then
	mkdir %{_sysconfdir}/opendkim
	chmod o-rx %{_sysconfdir}/opendkim
	opendkim-genkey -D %{_sysconfdir}/opendkim -s key -d `hostname --domain`
	chown -R opendkim:opendkim %{_sysconfdir}/opendkim
fi
if [ -x /sbin/chkconfig ]; then
	/sbin/chkconfig --add opendkim
elif [ -x /usr/lib/lsb/install_initd ]; then
	/usr/lib/lsb/install_initd opendkim
fi

%preun
if [ $1 = 0 ]; then
	service opendkim stop && rm -f %{_localstatedir}/run/opendkim/opendkim.sock && rmdir %{_localstatedir}/run/opendkim 2>/dev/null
	if [ -x /sbin/chkconfig ]; then
		/sbin/chkconfig --del opendkim
	elif [ -x /usr/lib/lsb/remove_initd ]; then
		/usr/lib/lsb/remove_initd opendkim
	fi
	userdel opendkim
	if getent group opendkim >/dev/null; then
		groupdel opendkim
	fi
fi

%clean
if [ "$RPM_BUILD_ROOT" != "/" ]; then
	rm -r "$RPM_BUILD_ROOT"
fi

%files
%defattr(-,root,root)
%doc FEATURES KNOWNBUGS LICENSE LICENSE.Sendmail README RELEASE_NOTES RELEASE_NOTES.Sendmail
%doc contrib/convert/convert_keylist.sh opendkim/*.sample
%doc opendkim/opendkim.conf.simple-verify opendkim/opendkim.conf.simple
%config(noreplace) %{_sysconfdir}/opendkim.conf
%config %{_initrddir}/%{name}
%{_mandir}/*/*
%{_sbindir}/*


%files -n libopendkim
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n libopendkim-devel
%defattr(-,root,root)
%doc libopendkim/docs/*.html
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
