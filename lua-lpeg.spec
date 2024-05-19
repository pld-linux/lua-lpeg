%define	__lua	/usr/bin/lua5.1
#define	luaver %(%{__lua} -e "print(string.sub(_VERSION, 5))")
%define	luaver 5.1
%define	lualibdir %{_libdir}/lua/%{luaver}
%define	luapkgdir %{_datadir}/lua/%{luaver}

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
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LPeg is a new pattern-matching library for Lua, based on Parsing
Expression Grammars (PEGs).

%prep
%setup -q -n lpeg-%{version}
%{__sed} -i -e "s|/usr/bin/env lua5.1|%{__lua}|" test.lua
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

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{lualibdir},%{luapkgdir}}

install -p lpeg.so $RPM_BUILD_ROOT%{lualibdir}/lpeg.so.%{version}
ln -s lpeg.so.%{version} $RPM_BUILD_ROOT%{lualibdir}/lpeg.so
install -p re.lua $RPM_BUILD_ROOT%{luapkgdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc HISTORY lpeg.html re.html lpeg-128.gif test.lua
%attr(755,root,root) %{lualibdir}/lpeg.so*
%{luapkgdir}/re.lua
