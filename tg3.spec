#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	up		# don't build UP module
%bcond_without	smp		# don't build SMP module
%bcond_without	userspace	# don't build userspace programs
%bcond_with	verbose		# verbose build (V=1)

%if %{without kernel}
%undefine	with_dist_kernel
%endif
%if "%{_alt_kernel}" != "%{nil}"
%undefine	with_userspace
%endif
%if %{without userspace}
# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0
%endif

%ifarch sparc
%undefine	with_smp
%endif

%define		rel		1
%define		pname	tg3
Summary:	Linux driver for the Broadcom's NetXtreme BCM57xx Network Interface Cards
Summary(pl.UTF-8):	Sterownik dla Linuksa do kart sieciowych Broadcom NetXtreme BCM57xx
Name:		%{pname}%{_alt_kernel}
Version:	3.92n
Release:	%{rel}
License:	GPL v2
Group:		Base/Kernel
Source0:	%{pname}-%{version}.tar.bz2
URL:		http://www.broadcom.com/drivers/downloaddrivers.php
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.14}
BuildRequires:	rpmbuild(macros) >= 1.452
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the Linux driver for the Broadcom's NetXtreme
BCM57xx Network Interface Cards.

%description -l pl.UTF-8
Pakiet zawiera sterownik dla Linuksa do kart sieciowych Broadcom
BCM57xx.

%package -n kernel%{_alt_kernel}-net-tg3
Summary:	Linux SMP driver for the Broadcom's NetXtreme BCM57xx Network Interface Cards
Summary(pl.UTF-8):	Sterownik dla Linuksa SMP do kart sieciowych Broadcom BCM57xx
Release:	%{rel}@%{_kernel_vermagic}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:Requires:	kernel%{_alt_kernel}(vermagic) = %{_kernel_ver}}

%description -n kernel%{_alt_kernel}-net-tg3
Linux driver for the Broadcom's NetXtreme BCM57xx Network Interface
Cards.

%description -n kernel%{_alt_kernel}-net-tg3 -l pl.UTF-8
Sterownik dla Linuksa do kart sieciowych Broadcom BCM57xx.

%package -n kernel%{_alt_kernel}-smp-net-tg3
Summary:	Linux SMP driver for the Broadcom's NetXtreme BCM57xx Network Interface Cards
Summary(pl.UTF-8):	Sterownik dla Linuksa SMP do kart sieciowych Broadcom BCM57xx
Release:	%{rel}@%{_kernel_vermagic}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:Requires:	kernel%{_alt_kernel}-smp(vermagic) = %{_kernel_ver}}

%description -n kernel%{_alt_kernel}-smp-net-tg3
Linux SMP driver for the Broadcom's NetXtreme BCM57xx Network
Interface Cards.

%description -n kernel%{_alt_kernel}-smp-net-tg3 -l pl.UTF-8
Sterownik dla Linuksa SMP do kart sieciowych Broadcom BCM57xx.

%prep
%setup -q -n %{pname}-%{version}

%build
./makeflags.sh /usr/src/linux > tg3_flags.h
%build_kernel_modules -m tg3

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
install -d $RPM_BUILD_ROOT%{_mandir}/man4
install tg3.4 $RPM_BUILD_ROOT%{_mandir}/man4
%endif

%if %{with kernel}
%install_kernel_modules -m tg3 -d kernel/drivers/net
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-net-tg3
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-net-tg3
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-smp-net-tg3
%depmod %{_kernel_ver}smp

%postun	-n kernel%{_alt_kernel}-smp-net-tg3
%depmod %{_kernel_ver}smp

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc README.TXT
%{_mandir}/man4/tg3.*
%endif

%if %{with kernel}
%if %{with up} || %{without dist_kernel}
%files -n kernel%{_alt_kernel}-net-tg3
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/net/tg3.ko*
%endif

%if %{with smp} && %{with dist_kernel}
%files -n kernel%{_alt_kernel}-smp-net-tg3
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/tg3.ko*
%endif
%endif
