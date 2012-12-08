%if %_lib == lib64
%define _requires_exceptions devel(libtcl8.4(64bit))
%else
%define _requires_exceptions devel(libtcl8.4)
%endif

%define Werror_cflags %nil
%define _disable_ld_no_undefined 1

%define perl_version %(rpm -q --qf "%{VERSION}" perl)
%define perl_epoch %(rpm -q --qf "%{EPOCH}" perl)

%define pgdata /var/lib/pgsql
%define logrotatedir %{_sysconfdir}/logrotate.d

%define major 5
%define major_ecpg 6

%define bname postgresql
%define current_major_version 9.0
%define current_minor_version 9

# Define if it's a beta
# %%define beta rc2

# define the mdv release
%define rel 0

%define subrel 1
%define release %mkrel %{?beta:0.rc.%{beta}.}%{rel}

%define libname %mklibname pq%{current_major_version} _%{major}
%define libecpg %mklibname ecpg%{current_major_version} _%{major_ecpg}

%define withuuid 0
%if %mdvver >= 201100
%define withuuid 1
%endif

Summary: 	PostgreSQL client programs and libraries
Name:		%{bname}%{current_major_version}
Version: 	%{current_major_version}%{?!beta:.%{current_minor_version}}
Release: 	%release
License:	BSD
Group:		Databases
URL:		http://www.postgresql.org/ 
Source0:	ftp://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}%{?beta}.tar.bz2
Source5:	ftp://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}%{?beta}.tar.bz2.md5
Source10:	postgres.profile
Source11:	postgresql.init
Source13:	postgresql.mdv.releasenote
Patch0:		postgresql-9.0.4_ossp-uuid-dir.patch
Patch1:		 postgresql-9.0.8-soname_fix.diff
Requires:	perl
Provides:	postgresql-clients = %{version}-%{release}
BuildRequires:	bison flex
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
BuildRequires:	perl-devel
BuildRequires:	python-devel
BuildRequires:	readline-devel
BuildRequires:	tcl-devel
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-devel
BuildRequires:	zlib-devel
%if %withuuid
BuildRequires:  ossp-uuid-devel >= 1.6.2-5
%endif
# Need to build doc
BuildRequires:  docbook-dtd42-sgml docbook-dtd44-xml
BuildRequires:	openjade docbook-utils xsltproc docbook-style-xsl
Provides:	%{bname}-virtual = %{current_major_version}
Conflicts:	%{bname}-virtual < %{current_major_version}
Requires:	%{libname} >= %{version}
Provides:	%{bname} = %{version}-%{release}
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
PostgreSQL is an advanced Object-Relational database management system (DBMS)
that supports almost all SQL constructs (including transactions, subselects and
user-defined types and functions). The postgresql package includes the client
programs and libraries that you'll need to access a PostgreSQL DBMS server.
These PostgreSQL client programs are programs that directly manipulate the
internal structure of PostgreSQL databases on a PostgreSQL server. These client
programs can be located on the same machine with the PostgreSQL server, or may
be on a remote machine which accesses a PostgreSQL server over a network
connection. This package contains the client libraries for C and C++, as well
as command-line utilities for managing PostgreSQL databases on a PostgreSQL
server.

If you want to manipulate a PostgreSQL database on a remote PostgreSQL server,
you need this package. You also need to install this package if you're
installing the postgresql-server package.

%package -n	%{libname}
Summary:	The shared libraries required for any PostgreSQL clients
Group:		System/Libraries
Provides:	postgresql-libs = %{version}-%{release}
Provides:	libpq = %{version}-%{release}
Provides:	%{mklibname pq}-virtual = %{current_major_version}
Conflicts:	postgresql-libs < %{current_major_version}
# Avoid conflicts with lib having bad major
Conflicts:	libpq3 = 8.0.2

%description -n	%{libname}
C and C++ libraries to enable user programs to communicate with the PostgreSQL
database backend. The backend can be on another machine and accessed through
TCP/IP.

%package -n	%{libecpg}
Summary:	Shared library libecpg for PostgreSQL
Group:		System/Libraries
Requires:	postgresql%{current_major_version} >= %{version}-%{release}
Provides:	libecpg = %{version}-%{release}
Provides:	%{mklibname ecpg}-virtual = %{current_major_version}
Conflicts:	libecpg < %{current_major_version}

%description -n	%{libecpg}
Libecpg is used by programs built with ecpg (Embedded PostgreSQL for C) Use
postgresql-dev to develop such programs.

%package	server
Summary:	The programs needed to create and run a PostgreSQL server
Group:		Databases
Provides:	sqlserver
Requires(post): %{libname} >= %{version}-%{release}
Requires(preun): %{libname} >= %{version}-%{release}
# add/remove services
Requires(post): rpm-helper
Requires(preun): rpm-helper
# add/del user
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	postgresql%{current_major_version} >= %{version}-%{release}
Requires(post):	postgresql%{current_major_version} >= %{version}-%{release}
Conflicts:	postgresql < 7.3
Provides:	%{?arch_tagged:%arch_tagged %{bname}-server-ABI}%{?!arch_tagged:%{bname}-server-ABI} = %{current_major_version}
Provides:	%{bname}-server-virtual = %{current_major_version}
Conflicts:	%{bname}-server-virtual < %{current_major_version}
Provides:	%{bname}-server = %{version}-%{release}
Conflicts:	%{bname}8.3-test < %{version}-%{release}
Requires:   postgresql-plpgsql >= %{version}-%{release}

%description	server
The postgresql-server package includes the programs needed to create and run a
PostgreSQL server, which will in turn allow you to create and maintain
PostgreSQL databases.  PostgreSQL is an advanced Object-Relational database
management system (DBMS) that supports almost all SQL constructs (including
transactions, subselects and user-defined types and functions). You should
install postgresql-server if you want to create and maintain your own
PostgreSQL databases and/or your own PostgreSQL server. You also need to
install the postgresql and postgresql-devel packages.

After installing this package, please read postgresql.mdv.releasenote.

%package	docs
Summary:	Extra documentation for PostgreSQL
Group:		Databases
Provides:	%{bname}-docs-virtual = %{current_major_version}
Conflicts:	%{bname}-docs-virtual < %{current_major_version}

%description	docs
The postgresql-docs package includes the SGML source for the documentation as
well as the documentation in other formats, and some extra documentation.
Install this package if you want to help with the PostgreSQL documentation
project, or if you want to generate printed documentation.

%package	contrib
Summary:	Contributed binaries distributed with PostgreSQL
Group:		Databases
Requires:	postgresql%{current_major_version}-server >= %{version}-%{release}
Provides:	%{bname}-contrib-virtual = %{current_major_version}
Conflicts:	%{bname}-contrib-virtual < %{current_major_version}

%description	contrib
The postgresql-contrib package includes the contrib tree distributed with the
PostgreSQL tarball.  Selected contrib modules are prebuilt.

%package	devel
Summary:	PostgreSQL development header files and libraries
Group:		Development/Databases
Requires:	postgresql%{current_major_version} >= %{version}-%{release}
Provides:	%{bname}-devel-virtual = %{current_major_version}
Conflicts:	%{bname}-devel-virtual < %{current_major_version}
Requires:	%{libname} >= %{version}-%{release}
Provides:	postgresql-libs-devel = %{version}-%{release}
Provides:	pq-devel = %{version}-%{release}
# Avoid conflicts with lib having bad major
Conflicts:	libpq3-devel = 8.0.2
%if %_lib != lib
Provides:	libpq-devel = %{version}-%{release}
%endif
Provides:	%{_lib}pq-devel = %{version}
Requires:	%{libecpg} >= %{version}-%{release}
Provides:	libecpg-devel = %{version}-%{release} 
Provides:	%{_lib}ecpg-devel = %{version}-%{release}
Conflicts:	%mklibname -d ecpg 5
Conflicts:	%mklibname -d pq 5
Conflicts:	%mklibname -d pq8.3
Conflicts:	%mklibname -d ecpg8.3
Conflicts:	%mklibname -d pq8.4
Conflicts:	%mklibname -d ecpg8.4
Provides:	%{bname}-devel = %{version}-%{release}

%description	devel
The postgresql-devel package contains the header files and libraries needed to
compile C or C++ applications which will directly interact with a PostgreSQL
database management server and the ecpg Embedded C Postgres preprocessor. You
need to install this package if you want to develop applications which will
interact with a PostgreSQL server. If you're installing postgresql-server, you
need to install this package.

%package	pl
Summary:	Procedurals languages for PostgreSQL
Group:		Databases
Conflicts:	libpgsql2
Requires:	%{name}-plpython >= %{version}-%{release} 
Requires:	%{name}-plperl >= %{version}-%{release} 
Requires:	%{name}-pltcl >= %{version}-%{release} 
Requires:	%{name}-plpgsql >= %{version}-%{release} 
Provides:	%{bname}-pl-virtual = %{current_major_version}
Conflicts:	%{bname}-pl-virtual < %{current_major_version}
Provides:	%{bname}-pl = %{version}-%{release}

%description	pl
PostgreSQL is an advanced Object-Relational database management system. The
postgresql-pl will install the the PL/Perl, PL/Tcl, and PL/Python procedural
languages for the backend. PL/Pgsql is part of the core server package.

%package	plpython
Summary:	The PL/Python procedural language for PostgreSQL
Group:		Databases
Requires:	postgresql%{current_major_version}-server >= %{version}
Requires:	%{?arch_tagged:%arch_tagged %{bname}-server-ABI}%{?!arch_tagged:%{bname}-server-ABI} >= %{current_major_version}
Provides:	%{bname}-plpython-virtual = %{current_major_version}
Conflicts:	%{bname}-plpython-virtual < %{current_major_version}
Provides:	%{bname}-plpython = %{version}-%{release}

%description	plpython
PostgreSQL is an advanced Object-Relational database management system. The
postgresql-plpython package contains the the PL/Python procedural languages for
the backend. PL/Python is part of the core server package.

%package	plperl
Summary:	The PL/Perl procedural language for PostgreSQL
Group:		Databases
Requires:	postgresql%{current_major_version}-server >= %{version}
Requires:	perl-base >= %{perl_epoch}:%{perl_version}
Requires:	%{?arch_tagged:%arch_tagged %{bname}-server-ABI}%{?!arch_tagged:%{bname}-server-ABI} >= %{current_major_version}
Provides:	%{bname}-plperl-virtual = %{current_major_version}
Conflicts:	%{bname}-plperl-virtual < %{current_major_version}
Provides:	%{bname}-plperl = %{version}-%{release}

%description	plperl
PostgreSQL is an advanced Object-Relational database management system. The
postgresql-plperl package contains the the PL/Perl procedural languages for the
backend. PL/Perl is part of the core server package.

%package	pltcl
Summary:	The PL/Tcl procedural language for PostgreSQL
Group:		Databases
Requires:	postgresql%{current_major_version}-server >= %{version}
Requires:	%{?arch_tagged:%arch_tagged %{bname}-server-ABI}%{?!arch_tagged:%{bname}-server-ABI} >= %{current_major_version}
Provides:	%{bname}-pltcl-virtual = %{current_major_version}
Conflicts:	%{bname}-pltcl-virtual < %{current_major_version}
Provides:	%{bname}-pltcl = %{version}-%{release}

%description	pltcl
PostgreSQL is an advanced Object-Relational database management system. The
postgresql-pltcl package contains the the PL/Tcl procedural languages for the
backend. PL/Tcl is part of the core server package.

%package	plpgsql
Summary:	The PL/PgSQL procedural language for PostgreSQL
Group:		Databases
Requires:	postgresql%{current_major_version}-server >= %{version}
Requires:	%{?arch_tagged:%arch_tagged %{bname}-server-ABI}%{?!arch_tagged:%{bname}-server-ABI} >= %{current_major_version}
Provides:	%{bname}-plpgsql-virtual = %{current_major_version}
Conflicts:	%{bname}-plpgsql-virtual < %{current_major_version}
Provides:	%{bname}-plpgsql = %{version}-%{release}

%description	plpgsql
PostgreSQL is an advanced Object-Relational database management system. The
postgresql-plpgsql package contains the the PL/PgSQL procedural languages for
the backend. PL/PgSQL is part of the core server package.

%prep

%setup -q -n %{bname}-%{version}%{?beta}
%patch0 -p1 -b .ossp-uuid_dir~
%patch1 -p1 -b .soname_fix

%build

%serverbuild
# it does not work with -fPIE and someone added that to the serverbuild macro...
CFLAGS=`echo $CFLAGS|sed -e 's|-fPIE||g'`
CXXFLAGS=`echo $CXXFLAGS|sed -e 's|-fPIE||g'`

%configure2_5x \
        --disable-rpath \
	--with-perl \
	--with-python \
        --with-tcl --with-tclconfig=%{_libdir} \
        --with-openssl \
        --with-pam \
        --with-libxml \
        --with-libxslt \
        --libdir=%{_libdir} \
        --mandir=%{_mandir} \
        --prefix=%_prefix \
        --sysconfdir=%{_sysconfdir}/pgsql \
        --enable-nls \
%if %withuuid
        --with-ossp-uuid
%endif

# nuke -Wl,--no-undefined
perl -pi -e "s|-Wl,--no-undefined||g" src/Makefile.global

%if %withuuid
# bork...
echo "#define HAVE_OSSP_UUID_H 1" >> src/include/pg_config.h
%endif

%make world

pushd src/test
make all
popd

%check
make check

%install
rm -rf %{buildroot}

make DESTDIR=%{buildroot} install-world install-docs

# install odbcinst.ini
mkdir -p %{buildroot}%{_sysconfdir}/pgsql

# copy over Makefile.global to the include dir....
#install -m755 src/Makefile.global %{buildroot}%{_includedir}/pgsql/

# PGDATA needs removal of group and world permissions due to pg_pwd hole.
install -d -m 700 %{buildroot}/var/lib/pgsql/data

# backups of data go here...
install -d -m 700 %{buildroot}/var/lib/pgsql/backups

# Create the multiple postmaster startup directory
install -d -m 700 %{buildroot}/etc/sysconfig/pgsql

%if 0
# tests. There are many files included here that are unnecessary, but include
# them anyway for completeness.
mkdir -p %{buildroot}%{_libdir}/pgsql/test
cp -a src/test/regress %{buildroot}%{_libdir}/pgsql/test
install -m 0755 contrib/spi/refint.so %{buildroot}%{_libdir}/pgsql/test/regress
install -m 0755 contrib/spi/autoinc.so %{buildroot}%{_libdir}/pgsql/test/regress
pushd  %{buildroot}%{_libdir}/pgsql/test/regress/
strip *.so
popd
%endif

mkdir -p %buildroot/var/log/postgres

mkdir -p %buildroot%logrotatedir
cat > %buildroot%logrotatedir/%{bname} <<EOF
/var/log/postgres/postgresql {
    notifempty
    missingok
    copytruncate
}
EOF

install -D -m755 %{SOURCE11} %{buildroot}%{_initrddir}/postgresql

mv %{buildroot}%{_docdir}/%{bname}/html %{buildroot}%{_docdir}/%{name}-docs-%{version}

echo -n '' > main.lst
for i in \
    pg_ctl initdb pg_config psql pg_dump pgscripts \
    ecpg libpq%{major} ecpglib%{major_ecpg}; do
    %find_lang $i-%{current_major_version}
    cat $i-%{current_major_version}.lang >> main.lst
#    %find_lang $i
#    cat $i.lang >> main.lst
done
echo -n '' > server.lst
for i in postgres pg_resetxlog pg_controldata plpgsql plpython plperl pltcl; do
#    %find_lang $i
#    cat $i.lang >> server.lst
    %find_lang $i-%{current_major_version}
    cat $i-%{current_major_version}.lang >> server.lst
done

# pg_ctl.lang initdb.lang pg_config.lang psql.lang pg_dump.lang pgscripts.lang \
# postgres.lang pg_resetxlog.lang pg_controldata.lang \
# libpq.lang libecpg.lang \

# taken directly in build dir.
rm -fr %{buildroot}%{_datadir}/doc/postgresql/contrib/

#(
#cd postgresql-mdk
#make install DESTDIR=%buildroot
#)

mkdir -p %buildroot/%_sys_macros_dir
cat > %buildroot/%_sys_macros_dir/%{name}.macros <<EOF
%%postgresql_version %{version}
%%postgresql_major   %{current_major_version}
%%postgresql_minor   %{current_minor_version}
%%pgmodules_req Requires: %{?arch_tagged:%arch_tagged %{bname}-server-ABI}%{?!arch_tagged:%{bname}-server-ABI} >= %{current_major_version}
EOF

cat %{SOURCE13} > postgresql.mdv.releasenote
cat > README.urpmi <<EOF
You just installed or updated %{bname} server.
You can find important information about mandriva %{bname} rpms and database
management in:

%{_defaultdocdir}/%{name}-server/postgresql.mdv.releasenote

Please read it.
EOF

# postgres' .profile and .bashrc
install -D -m 700 %SOURCE10 %{buildroot}/var/lib/pgsql/.profile
(
cd %{buildroot}/var/lib/pgsql/
ln -s .profile .bashrc
)

cat > %buildroot%_sysconfdir/sysconfig/postgresql <<EOF
# Olivier Thauvin <nanardon@mandriva.org>

# The database location:
# You probably won't change this
# PGDATA=/var/lib/pgsql/data

# What is the based locales for postgresql
# Setting locales to C allow to use any encoding
# ISO or UTF, any other choice will restrict you
# either ISO or UTF.
LC_ALL=C

# These are additional to pass to pg_ctl when starting/restarting postgresql.
# PGOPTIONS=
EOF

%pre server
%_pre_useradd postgres /var/lib/pgsql /bin/bash

[ ! -f %pgdata/data/PG_VERSION ] && exit 0
mypgversion=`cat %pgdata/data/PG_VERSION`
[ $mypgversion = %{current_major_version} ] && exit 0

echo ""
echo "You currently have database tree for Postgresql $mypgversion"
echo "You must use postgresql${mypgversion}-server"
echo "To update you Postgresql server, dump your databases"
echo "delete /var/lib/pgsql/data/ content, upgrade the server, then"
echo "restore your databases from your backup"
echo ""

exit 1

%posttrans server

%_post_service %{bname}

%preun server
%_preun_service %{bname}

%postun server
%_postun_userdel postgres

%clean
rm -rf %{buildroot}

%files -f main.lst
%defattr(-,root,root)
%doc doc/KNOWN_BUGS doc/MISSING_FEATURES doc/README* 
%doc COPYRIGHT README HISTORY doc/bug.template
%{_bindir}/clusterdb
%{_bindir}/createdb
%{_bindir}/createlang
%{_bindir}/createuser
%{_bindir}/dropdb
%{_bindir}/droplang
%{_bindir}/dropuser
%{_bindir}/pg_dump
%{_bindir}/pg_dumpall
%{_bindir}/pg_restore
%{_bindir}/psql
%{_bindir}/reindexdb
%{_bindir}/vacuumdb
%{_mandir}/man1/clusterdb.*
%{_mandir}/man1/createdb.*
%{_mandir}/man1/createlang.*
%{_mandir}/man1/createuser.*
%{_mandir}/man1/dropdb.*
%{_mandir}/man1/droplang.*
%{_mandir}/man1/dropuser.*
%{_mandir}/man1/pg_dump.*
%{_mandir}/man1/pg_dumpall.*
%{_mandir}/man1/pg_restore.*
%{_mandir}/man1/psql.*
%{_mandir}/man1/vacuumdb.*
%{_mandir}/man1/reindexdb.*
%{_mandir}/man7/*
%_sys_macros_dir/%{name}.macros

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libpq.so.%{major}*

%files -n %{libecpg}
%defattr(-,root,root)
%{_libdir}/libecpg.so.%{major_ecpg}*
%{_libdir}/libecpg_compat.so.*
%{_libdir}/libpgtypes.so.*

%files docs
%defattr(-,root,root)
%doc %{_docdir}/%{name}-docs-%{version}

%files contrib
%defattr(-,root,root)
# %doc contrib/*/README.* contrib/spi/*.example
%{_libdir}/postgresql/_int.so
%{_libdir}/postgresql/btree_gist.so
%{_libdir}/postgresql/chkpass.so
%{_libdir}/postgresql/cube.so
%{_libdir}/postgresql/dblink.so
%{_libdir}/postgresql/earthdistance.so
%{_libdir}/postgresql/fuzzystrmatch.so
%{_libdir}/postgresql/insert_username.so
%{_libdir}/postgresql/lo.so
%{_libdir}/postgresql/ltree.so
%{_libdir}/postgresql/moddatetime.so
%{_libdir}/postgresql/pgcrypto.so
%{_libdir}/postgresql/pgstattuple.so
%{_libdir}/postgresql/refint.so
%{_libdir}/postgresql/seg.so
%{_libdir}/postgresql/tablefunc.so
%{_libdir}/postgresql/timetravel.so
%{_libdir}/postgresql/pg_trgm.so
%{_libdir}/postgresql/autoinc.so
%{_libdir}/postgresql/pg_buffercache.so
%{_libdir}/postgresql/adminpack.so
%{_libdir}/postgresql/hstore.so
%{_libdir}/postgresql/isn.so
%{_libdir}/postgresql/pg_freespacemap.so
%{_libdir}/postgresql/pgrowlocks.so
%{_libdir}/postgresql/sslinfo.so
%{_libdir}/postgresql/pageinspect.so

%{_datadir}/postgresql/contrib/
%{_bindir}/oid2name
%{_bindir}/pgbench
%{_bindir}/vacuumlo

%files server -f server.lst
%defattr(-,root,root)
%{_initrddir}/postgresql
%config(noreplace) %{_sysconfdir}/sysconfig/postgresql
%doc README.urpmi postgresql.mdv.releasenote
%{_bindir}/initdb
%{_bindir}/pg_controldata
%{_bindir}/pg_ctl
%{_bindir}/pg_resetxlog
%{_bindir}/postgres
%{_bindir}/postmaster
%{_bindir}/pg_standby
%{_bindir}/pg_archivecleanup
%{_bindir}/pg_upgrade
%{_mandir}/man1/initdb.1*
%{_mandir}/man1/pg_controldata.*
%{_mandir}/man1/pg_ctl.1*
%{_mandir}/man1/pg_resetxlog.*
%{_mandir}/man1/postgres.1*
%{_mandir}/man1/postmaster.1*
%dir %{_libdir}/postgresql
%dir %{_datadir}/postgresql
%attr(644,postgres,postgres) %config(noreplace) /var/lib/pgsql/.bashrc
%attr(-,postgres,postgres) /var/lib/pgsql/.profile
%attr(700,postgres,postgres) %dir %{pgdata}
%attr(-,postgres,postgres) %{pgdata}/data
%attr(700,postgres,postgres) %dir %{pgdata}/backups
%{_libdir}/postgresql/*_and_*.so
%{_libdir}/postgresql/pgxml.so
%{_libdir}/postgresql/dict_int.so
%{_libdir}/postgresql/dict_xsyn.so
%{_libdir}/postgresql/test_parser.so
%{_libdir}/postgresql/tsearch2.so
%{_libdir}/postgresql/dict_snowball.so
%{_libdir}/postgresql/auto_explain.so
%{_libdir}/postgresql/btree_gin.so
%{_libdir}/postgresql/citext.so
%{_libdir}/postgresql/pg_stat_statements.so
%if %withuuid
%{_libdir}/postgresql/uuid-ossp.so
%endif
%{_libdir}/postgresql/euc2004_sjis2004.so
%{_libdir}/postgresql/libpqwalreceiver.so
%{_libdir}/postgresql/passwordcheck.so
%{_libdir}/postgresql/pg_upgrade_support.so
%{_libdir}/postgresql/unaccent.so
%{_datadir}/postgresql/postgres.bki
%{_datadir}/postgresql/postgres.description
%{_datadir}/postgresql/*.sample
%{_datadir}/postgresql/timezone
%{_datadir}/postgresql/system_views.sql
%{_datadir}/postgresql/conversion_create.sql
%{_datadir}/postgresql/information_schema.sql
%{_datadir}/postgresql/snowball_create.sql
%{_datadir}/postgresql/sql_features.txt
%{_datadir}/postgresql/postgres.shdescription
%dir %{_datadir}/postgresql/timezonesets
%{_datadir}/postgresql/timezonesets/Africa.txt
%{_datadir}/postgresql/timezonesets/America.txt
%{_datadir}/postgresql/timezonesets/Antarctica.txt
%{_datadir}/postgresql/timezonesets/Asia.txt
%{_datadir}/postgresql/timezonesets/Atlantic.txt
%{_datadir}/postgresql/timezonesets/Australia
%{_datadir}/postgresql/timezonesets/Australia.txt
%{_datadir}/postgresql/timezonesets/Default
%{_datadir}/postgresql/timezonesets/Etc.txt
%{_datadir}/postgresql/timezonesets/Europe.txt
%{_datadir}/postgresql/timezonesets/India
%{_datadir}/postgresql/timezonesets/Indian.txt
%{_datadir}/postgresql/timezonesets/Pacific.txt
%{_datadir}/postgresql/tsearch_data

%attr(700,postgres,postgres) %dir /var/log/postgres
%logrotatedir/%{bname}

%files devel
%defattr(-,root,root)
# %doc doc/TODO doc/TODO.detail
%{_includedir}/*
%{_bindir}/ecpg
%{_libdir}/lib*.a
%{_libdir}/lib*.so
%{_libdir}/postgresql/pgxs/
%{_mandir}/man1/ecpg.1*
%{_bindir}/pg_config
%{_mandir}/man1/pg_config.1*
#From %files -n %{libnamedevel}
#%{_libdir}/libpq.so
#From %files -n %{libecpgdevel}
#%{_libdir}/libecpg.so
%{_mandir}/man3/SPI_*.3*
%{_mandir}/man3/dblink*.3*

%files pl 
%defattr(-,root,root) 

%files plpython
%defattr(-,root,root) 
%{_libdir}/postgresql/plpython.so
%{_libdir}/postgresql/plpython2.so

%files plperl
%defattr(-,root,root) 
%{_libdir}/postgresql/plperl.so

%files pltcl
%defattr(-,root,root) 
%{_libdir}/postgresql/pltcl.so
%{_bindir}/pltcl_delmod 
%{_bindir}/pltcl_listmod 
%{_bindir}/pltcl_loadmod 
%{_datadir}/postgresql/unknown.pltcl

%files plpgsql
%defattr(-,root,root) 
%{_libdir}/postgresql/plpgsql.so


%changelog
* Tue Aug 21 2012 Danila Leontiev <danila.leontiev@rosalab.ru>  9.0.9-0.1
- 9.0.9: nnew upstream maintenance version, fixes CVE-2012-3488, CVE-2012-3489

* Wed Jun 20 2012 Danila Leontiev <danila.leontiev@rosalab.ru>  9.0.8-0.1
- 9.0.8: new upstream maintenance version, fixes CVE-2012-2143, CVE-2012-2655

* Wed Feb 29 2012 Oden Eriksson <oeriksson@mandriva.com> 9.0.7-0.1
- 9.0.7: new upstream maintenance version, fixes CVE-2012-0866,0867,0868

* Mon Oct 24 2011 Oden Eriksson <oeriksson@mandriva.com> 9.0.5-0.1
- 9.0.5: new upstream maintenance version, fixes CVE-2011-2483

* Thu Oct 06 2011 Oden Eriksson <oeriksson@mandriva.com> 9.0.5-1mdv2012.0
+ Revision: 703338
- fix build
- 9.0.5

  + Matthew Dawkins <mattydaw@mandriva.org>
    - added p0 for ossp-uuid header dir
    - added missing BR docbook-dtd44-xml
    - fixed BR for ossp-uuid

* Sat Apr 23 2011 Funda Wang <fwang@mandriva.org> 9.0.4-1
+ Revision: 656791
- New verison 9.0.4

* Thu Mar 24 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 9.0.3-3
+ Revision: 648409
- add buildrequires on recent enough ossp_uuid-devel
- rebuild against renamed libossp-uuid library

* Sat Feb 26 2011 Götz Waschk <waschk@mandriva.org> 9.0.3-2
+ Revision: 639832
- rebuild for new perl

* Thu Feb 03 2011 Funda Wang <fwang@mandriva.org> 9.0.3-1
+ Revision: 635681
- BR docbook-style-xsl for manpage generation
- new version 9.0.3

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - fix conflicts on older versions

* Sat Jan 22 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 9.0.2-2
+ Revision: 632145
- drop overeager, redundant conflicts (#57689)

  + Funda Wang <fwang@mandriva.org>
    - tighten BR

* Thu Dec 30 2010 Oden Eriksson <oeriksson@mandriva.com> 9.0.2-1mdv2011.0
+ Revision: 626580
- 9.0.2

* Mon Nov 29 2010 Oden Eriksson <oeriksson@mandriva.com> 9.0.1-4mdv2011.0
+ Revision: 603112
- fix #61220 (MCC (drakconf) does not show correct status for postgresql, whether invoked by init.d or manually)

* Fri Oct 29 2010 Oden Eriksson <oeriksson@mandriva.com> 9.0.1-3mdv2011.0
+ Revision: 589943
- rebuild

* Thu Oct 28 2010 Olivier Thauvin <nanardon@mandriva.org> 9.0.1-2mdv2011.0
+ Revision: 589654
- plpgsql is now need by server

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - don't tag init script as a config file

* Tue Oct 05 2010 Oden Eriksson <oeriksson@mandriva.com> 9.0.1-1mdv2011.0
+ Revision: 583092
- import postgresql9.0


* Tue Oct 05 2010 Oden Eriksson <oeriksson@mandriva.com> 9.0.1-1mdv2010.1
- first cut at 9.x

* Mon Sep 20 2010 Per Øyvind Karlsen <peroyvind@mandriva.org> 8.4.4-8mdv2011.0
+ Revision: 580305
- fix the immediate stop mode in init script
- make sure to use log file when restarting

* Thu Sep 16 2010 Per Øyvind Karlsen <peroyvind@mandriva.org> 8.4.4-7mdv2011.0
+ Revision: 579081
- drop redundant(/broken, #55810) conflicts on future releases (real fix #57689)
- rewrite init script:
  	o use postgresql's own pid file
  	o fix locale usage so that database initialized uses sysconfig's LC_ALL
  	o add proper (LSB conforming) return codes
  	o allow starting even without network, as unix sockets can be used
  	o allow for specifying stop mode
  	o add condstop & condrestart
  	o add support for specifying additional pg_ctl start/restart arguments
  	o ditch attempts at cross-distro logics, mdv specific functioniality
  	  were already in use anyways..
  	o cosmetics!
- do not remove any existing postgresql unix sockets before starting, it's not
  necessary and will also remove sockets for any other running postgresql servers

* Thu Sep 09 2010 Olivier Thauvin <nanardon@mandriva.org> 8.4.4-6mdv2011.0
+ Revision: 576981
- rebuild for perl

* Mon Aug 23 2010 Olivier Thauvin <nanardon@mandriva.org> 8.4.4-5mdv2011.0
+ Revision: 572439
- make --with-ossp-uuid enable only on recent mdv to allow backport on mdv w/o ossp_uuid-devel

* Thu Jul 29 2010 Olivier Thauvin <nanardon@mandriva.org> 8.4.4-4mdv2011.0
+ Revision: 562900
- rebuild for new perl

* Thu Jul 22 2010 Olivier Thauvin <nanardon@mandriva.org> 8.4.4-3mdv2011.0
+ Revision: 556751
- rebuild for new perl

* Sat Jul 10 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 8.4.4-2mdv2011.0
+ Revision: 550319
- UUID function support

* Thu May 20 2010 Oden Eriksson <oeriksson@mandriva.com> 8.4.4-1mdv2010.1
+ Revision: 545480
- 8.4.4

  + Christophe Fergeau <cfergeau@mandriva.com>
    - fix typos in README.urpmi

* Mon Apr 05 2010 Funda Wang <fwang@mandriva.org> 8.4.3-2mdv2010.1
+ Revision: 531723
- rebuild for new openssl

* Tue Mar 16 2010 Funda Wang <fwang@mandriva.org> 8.4.3-1mdv2010.1
+ Revision: 520671
- New version 8.4.3

* Fri Feb 26 2010 Oden Eriksson <oeriksson@mandriva.com> 8.4.2-4mdv2010.1
+ Revision: 511620
- rebuilt against openssl-0.9.8m

* Wed Feb 17 2010 Olivier Thauvin <nanardon@mandriva.org> 8.4.2-3mdv2010.1
+ Revision: 507320
- dont provide libpq = ver-rel on 32bits system (#57689)

* Wed Feb 17 2010 Oden Eriksson <oeriksson@mandriva.com> 8.4.2-2mdv2010.1
+ Revision: 507077
- attempt to fix #57689 (postgresql8.4-devel conflicts with itself)

* Tue Dec 15 2009 Oden Eriksson <oeriksson@mandriva.com> 8.4.2-1mdv2010.1
+ Revision: 478953
- 8.4.2

* Mon Nov 23 2009 Olivier Thauvin <nanardon@mandriva.org> 8.4.1-2mdv2010.1
+ Revision: 469190
- redo define broke in last commit

* Wed Sep 09 2009 Frederik Himpe <fhimpe@mandriva.org> 8.4.1-1mdv2010.0
+ Revision: 435899
- update to new version 8.4.1
- Fix typo in source URL

* Wed Aug 26 2009 Götz Waschk <waschk@mandriva.org> 8.4.0-3mdv2010.0
+ Revision: 421514
- rebuild for new perl

* Wed Jul 29 2009 Olivier Thauvin <nanardon@mandriva.org> 8.4.0-2mdv2010.0
+ Revision: 402899
- add message about installation failure

* Fri Jul 03 2009 Olivier Thauvin <nanardon@mandriva.org> 8.4.0-1mdv2010.0
+ Revision: 391856
- 8.4.0 finale

* Sun Jun 28 2009 Olivier Thauvin <nanardon@mandriva.org> 8.4-0.rc.rc2.1mdv2010.0
+ Revision: 390132
- rc 2

* Fri May 22 2009 Olivier Thauvin <nanardon@mandriva.org> 8.4-0.rc.beta2.1mdv2010.0
+ Revision: 378727
- beta2

* Sat Apr 18 2009 Olivier Thauvin <nanardon@mandriva.org> 8.4-0.rc.beta1.1mdv2009.1
+ Revision: 367965
- postgres 8.4 (beta)
- 8.3.7
- cleanup initscripts: don't setup tcp port anymore, should be set in postgresql.conf
- by default /etc/syconfig/postgres is provided and force locales to C to allow multiple base encoding
- update mandriva release note
- 8.3.6
- rebuild for python
- patch1: fix printf fmt errors
- 8.3.5
- fix #44554 (typo in deps)
- try to make urpmi working
- avoid urpmi bugs with obsoletes
- force reupload
- replace obsoletes by conflicts
- kill obsoletes
- kill useless obsolete
- 8.3.4
- fix deps
- -server don't obsolete postgresql but -server package (pointed by Anssi)
- improve conflicts with other version
- fix paths
- kill test subpackage (not usefull)
- kill db migration script
- kill db migration script
- move C headers files to standard location
- fix /var location
- fix spec to comply to new non standard rpm behavior
- make localstatedir macro backportable
- 8.3.3
- fix typo in initscript
- 8.3.1
- move dict_snowball module from contrib to server, now required by main part
- initdb is now log into /var/log/postgres instead... /dev/null
- language provide pg-LANGUAGE
- obsolete old language package (#35374)
- merge all devel packages in pg-devel one (#27719)
- 8.3 is default for mdv 2008.1
- 8.3.0 final
- 8.3.0 RC2
- rebuild for perl 5.10
- 8.3 RC1
- fix dox path in help
- 8.3 beta4
- 8.3 beta 3
- 8.3 beta2
- kill bogus and useless data version check
- enable xml and xslt features
- kill old and useless now patch11
- another deps fix
- provide schema with the server
- fix services setup in scriptlets
- fix various dependencies
- versionned lib* to avoid clash with older version when major are the same
- postgresql 8.3 beta1
- fork for 8.3
- 8.2.5
- rebuild
- fix upgrade from 'postgresql'
- add conflicts to ensure clean upgrade
- provide empty package to pull latest
- Create postgresql8.2

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild for new libreadline
    - kill re-definition of %%buildroot on Pixel's request
    - buildrequires X11-devel instead of XFree86-devel

  + Adam Williamson <awilliamson@mandriva.org>
    - rebuild for new tcl

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers
    - normalize call to ldconfig in %%post/%%postun
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Oden Eriksson <oeriksson@mandriva.com>
    - bump release due to package loss

  + Anssi Hannula <anssi@mandriva.org>
    - rebuild for new soname of tcl

  + David Walluck <walluck@mandriva.org>
    - Provides: pq-devel = %%{version}-%%{release}

