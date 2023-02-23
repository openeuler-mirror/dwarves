%define libname libdwarves
%define libver 1
%define libbpfver 393a058

Name: dwarves
Version: 1.22
Release: 2
License: GPLv2
Summary: Debugging Information Manipulation Tools
URL: http://acmel.wordpress.com
Source: http://github.com/acmel/dwarves/archive/v%{version}.tar.gz
Source1: http://github.com/libbpf/libbpf/archive/%{libbpfver}.tar.gz
Requires: %{libname}%{libver} = %{version}-%{release}
BuildRequires: gcc
BuildRequires: cmake
BuildRequires: zlib-devel
BuildRequires: elfutils-devel >= 0.170

Patch0: replace-deprecated-libbpf-APIs-with-new-ones.patch
Patch1: backport-dwarf_loader-Support-DW_TAG_label-outside-DW_TAG_lex.patch

%description
dwarves is a set of tools that use the debugging information inserted in
ELF binaries by compilers such as GCC, used by well known debuggers such as
GDB, and more recent ones such as systemtap.

%package -n %{libname}%{libver}
Summary: Debugging information  processing library

%description -n %{libname}%{libver}
Debugging information processing library.

%package -n %{libname}%{libver}-devel
Summary: Debugging information library development files
Requires: %{libname}%{libver} = %{version}-%{release}

%description -n %{libname}%{libver}-devel
Debugging information processing library development files.

%prep
%autosetup -p1 -n %{name}-%{version}
tar -zxvf %{SOURCE1} --strip-components 1 -C %{_builddir}/%{name}-%{version}/lib/bpf/

%build
# Remove _FORTIFY_SOURCE from CFLAGS or else will get below error:
# error: #warning _FORTIFY_SOURCE requires compiling with optimization (-O) [-Werror=cpp]
export CFLAGS=$(echo %optflags | sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//g')

%cmake .
make VERBOSE=1 %{?_smp_mflags}

%install
rm -Rf %{buildroot}
make install DESTDIR=%{buildroot}

%ldconfig_scriptlets -n %{libname}%{libver}

%files
%doc README.ctracer
%doc README.btf
%doc changes-v1.17
%doc NEWS
%{_bindir}/*
%dir %{_datadir}/dwarves/
%dir %{_datadir}/dwarves/runtime/
%dir %{_datadir}/dwarves/runtime/python/
%defattr(0644,root,root,0755)
%{_mandir}/man1/pahole.1*
%{_datadir}/dwarves/runtime/Makefile
%{_datadir}/dwarves/runtime/linux.blacklist.cu
%{_datadir}/dwarves/runtime/ctracer_relay.c
%{_datadir}/dwarves/runtime/ctracer_relay.h
%attr(0755,root,root) %{_datadir}/dwarves/runtime/python/ostra.py*

%files -n %{libname}%{libver}
%{_libdir}/%{libname}.so.*
%{_libdir}/%{libname}_emit.so.*
%{_libdir}/%{libname}_reorganize.so.*

%files -n %{libname}%{libver}-devel
%doc MANIFEST README
%{_includedir}/*
%{_libdir}/%{libname}.so
%{_libdir}/%{libname}_emit.so
%{_libdir}/%{libname}_reorganize.so

%changelog
* Mon Mar 21 2022 - Kai Liu <kai.liu@suse.com> - 1.22-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC: Fix spew of warnings if build kernel with LLVM and
  CONFIG_DEBUG_INFO_BTF after commit 32ef9e5054ec
  ("Makefile.debug: re-enable debug info for .S files")

* Mon Mar 21 2022 - Kai Liu <kai.liu@suse.com> - 1.22-1
- Upgrade to v1.22. Also upgrade bundled libbpf to commit 393a058,
  the same as upstream submodule version.
  Introduce a patch from upstream commit 73383b3a3 to avoid using
  deprecated libbpf APIs.

* Mon May 24 2021 xiaqirong <xiaqirong1@huawei.com> - 1.17-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:bugfix about stopping using the deprecated mallinfo function 

* Wed Sep 16 2020 xiaqirong <xiaqirong1@huawei.com> - 1.17-1
- Type:package init
- ID:NA
- SUG:NA
- DESC:add dwarves package
