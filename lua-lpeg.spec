#
# Conditional build:
%bcond_without	luajit	# LuaJIT package

%define	__lua		/usr/bin/lua5.1
%define	luaver		5.1
%define	lualibdir	%{_libdir}/lua/%{luaver}
%define	luapkgdir	%{_datadir}/lua/%{luaver}

%define	__luajit	/usr/bin/luajit
%define	luajitabi	2.1
%define	luajitlibdir	%{_libdir}/luajit/%{luajitabi}
%define	luajitpkgdir	%{_datadir}/luajit/%{luajitabi}

%ifnarch %{ix86} %{x8664} %{arm} aarch64 mips mips64 mipsel ppc
%undefine	with_luajit
%endif

Summary:	Parsing Expression Grammars for Lua
Name:		lua-lpeg
Version:	1.1.0
Release:	1
License:	MIT
Group:		Development/Libraries
Source0:	https://www.inf.puc-rio.br/~roberto/lpeg/lpeg-%{version}.tar.gz
# Source0-md5:	842a538b403b5639510c9b6fffd2c75b
URL:		https://www.inf.puc-rio.br/~roberto/lpeg/
BuildRequires:	lua51 >= %{luaver}
BuildRequires:	lua51-devel >= %{luaver}
%if %{with luajit}
BuildRequires:	luajit >= %{luajitabi}
BuildRequires:	luajit-devel >= %{luajitabi}
%endif
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LPeg is a new pattern-matching library for Lua, based on Parsing
Expression Grammars (PEGs).

%package -n luajit-lpeg
Summary:	Parsing Expression Grammars for Lua
Requires:	luajit-libs

%description -n luajit-lpeg
LPeg is a new pattern-matching library for Lua, based on Parsing
Expression Grammars (PEGs).

%prep
%setup -q -n lpeg-%{version}
# strict module not part of our Lua 5.1.4
%{__sed} -i -e 's|require"strict"|-- require"strict"|' test.lua
%{__chmod} -x test.lua

%build
%{__make} lpeg.so \
	CC="%{__cc}" \
	COPT="%{rpmcflags}" \
	LUADIR=$(pkg-config --variable includedir lua%{luaver}) \
	DLLFLAGS="%{rpmldflags} -shared -fPIC $(pkg-config --libs lua%{luaver})"

%if %{with tests}
%{__lua} test.lua
%endif

install -D lpeg.so build-%{luaver}/lpeg.so

%if %{with luajit}
%{__make} clean

%{__make} lpeg.so \
	CC="%{__cc}" \
	COPT="%{rpmcflags}" \
	LUADIR=$(pkg-config --variable includedir luajit) \
	DLLFLAGS="%{rpmldflags} -shared -fPIC $(pkg-config --libs luajit)"

%if %{with tests}
%{__luajit} test.lua
%endif

install -D lpeg.so build-luajit/lpeg.so
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{lualibdir},%{luapkgdir},%{luajitlibdir},%{luajitpkgdir}}

install -p build-%{luaver}/lpeg.so $RPM_BUILD_ROOT%{lualibdir}/lpeg.so.%{version}
ln -s lpeg.so.%{version} $RPM_BUILD_ROOT%{lualibdir}/lpeg.so
install -p re.lua $RPM_BUILD_ROOT%{luapkgdir}

%if %{with luajit}
install -p build-luajit/lpeg.so $RPM_BUILD_ROOT%{luajitlibdir}/lpeg.so.%{version}
ln -s lpeg.so.%{version} $RPM_BUILD_ROOT%{luajitlibdir}/lpeg.so
install -p re.lua $RPM_BUILD_ROOT%{luajitpkgdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc HISTORY lpeg.html re.html lpeg-128.gif test.lua
%attr(755,root,root) %{lualibdir}/lpeg.so*
%{luapkgdir}/re.lua

%if %{with luajit}
%files -n luajit-lpeg
%defattr(644,root,root,755)
%doc HISTORY lpeg.html re.html lpeg-128.gif test.lua
%attr(755,root,root) %{luajitlibdir}/lpeg.so*
%{luajitpkgdir}/re.lua
%endif
