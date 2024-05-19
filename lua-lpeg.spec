%define	__lua		/usr/bin/lua5.1
%define	luaver		5.1
%define	lualibdir	%{_libdir}/lua/%{luaver}
%define	luapkgdir	%{_datadir}/lua/%{luaver}

%define	__luajit	/usr/bin/luajit
%define	luajitabi	2.1
%define	luajitlibdir	%{_libdir}/luajit/%{luajitabi}
%define	luajitpkgdir	%{_datadir}/luajit/%{luajitabi}

Summary:	Parsing Expression Grammars for Lua
Name:		lua-lpeg
Version:	1.1.0
Release:	1
License:	MIT
Group:		Development/Libraries
Source0:	http://www.inf.puc-rio.br/~roberto/lpeg/lpeg-%{version}.tar.gz
# Source0-md5:	842a538b403b5639510c9b6fffd2c75b
URL:		http://www.inf.puc-rio.br/~roberto/lpeg/
BuildRequires:	lua51 >= %{luaver}
BuildRequires:	lua51-devel >= %{luaver}
BuildRequires:	luajit >= %{luajitabi}
BuildRequires:	luajit-devel >= %{luajitabi}
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
	DLLFLAGS="-shared -fPIC $(pkg-config --libs lua%{luaver})"

%if %{with tests}
%{__lua} test.lua
%endif

install -D lpeg.so build-%{luaver}/lpeg.so

%{__make} clean

%{__make} lpeg.so \
	CC="%{__cc}" \
	COPT="%{rpmcflags}" \
	LUADIR=$(pkg-config --variable includedir luajit) \
	DLLFLAGS="-shared -fPIC $(pkg-config --libs luajit)"

%if %{with tests}
%{__luajit} test.lua
%endif

install -D lpeg.so build-luajit/lpeg.so

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{lualibdir},%{luapkgdir},%{luajitlibdir},%{luajitpkgdir}}

install -p build-%{luaver}/lpeg.so $RPM_BUILD_ROOT%{lualibdir}/lpeg.so.%{version}
ln -s lpeg.so.%{version} $RPM_BUILD_ROOT%{lualibdir}/lpeg.so
install -p re.lua $RPM_BUILD_ROOT%{luapkgdir}

install -p build-luajit/lpeg.so $RPM_BUILD_ROOT%{luajitlibdir}/lpeg.so.%{version}
ln -s lpeg.so.%{version} $RPM_BUILD_ROOT%{luajitlibdir}/lpeg.so
install -p re.lua $RPM_BUILD_ROOT%{luajitpkgdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc HISTORY lpeg.html re.html lpeg-128.gif test.lua
%attr(755,root,root) %{lualibdir}/lpeg.so*
%{luapkgdir}/re.lua

%files -n luajit-lpeg
%defattr(644,root,root,755)
%doc HISTORY lpeg.html re.html lpeg-128.gif test.lua
%attr(755,root,root) %{luajitlibdir}/lpeg.so*
%{luajitpkgdir}/re.lua
