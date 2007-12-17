%define section free
%define gcj_support 1

%define manual  0

Name:           bcel5.3
Version:        5.3
Release:        %mkrel 1.1.3
Epoch:          0
Summary:        Byte Code Engineering Library
License:        Apache License
# svn co -r417157 http://svn.apache.org/repos/asf/jakarta/bcel/trunk bcel
Source0:        http://www.apache.org/dist/jakarta/bcel/source/bcel.tar.bz2
Source1:        %{name}-jpp-depmap.xml
URL:            http://jakarta.apache.org/bcel/
Group:          Development/Java
BuildRequires:  java-rpmbuild >= 0:1.5
BuildRequires:  junit
BuildRequires:  maven2-plugin-compiler
BuildRequires:  maven2-plugin-install
BuildRequires:  maven2-plugin-jar
BuildRequires:  maven2-plugin-javadoc
BuildRequires:  maven2-plugin-resources
BuildRequires:  maven2-plugin-site
BuildRequires:  maven2-plugin-surefire
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
Buildarch:      noarch
%endif

%description
The Byte Code Engineering Library (formerly known as JavaClass) is
intended to give users a convenient possibility to analyze, create, and
manipulate (binary) Java class files (those ending with .class). Classes
are represented by objects which contain all the symbolic information of
the given class: methods, fields and byte code instructions, in
particular.  Such objects can be read from an existing file, be
transformed by a program (e.g. a class loader at run-time) and dumped to
a file again. An even more interesting application is the creation of
classes from scratch at run-time. The Byte Code Engineering Library
(BCEL) may be also useful if you want to learn about the Java Virtual
Machine (JVM) and the format of Java .class files.  BCEL is already
being used successfully in several projects such as compilers,
optimizers, obsfuscators and analysis tools, the most popular probably
being the Xalan XSLT processor at Apache.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%if %manual
%package manual
Summary:        Manual for %{name}
Group:          Development/Java

%description manual
Documentation for %{name}.
%endif

%prep
%setup -q -n bcel

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

mvn-jpp \
    -e \
    -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
    -Dmaven2-jpp.depmap.file=%{SOURCE1} \
    install javadoc:javadoc

%install
%{__rm} -rf %{buildroot}
# jars
%{__mkdir_p} %{buildroot}%{_javadir}
%{__install} -m 644 target/bcel-%{version}*.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do %{__ln_s} ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)
# javadoc
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && %{__ln_s} %{name}-%{version} %{name})
%{__rm} -rf docs/api

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc LICENSE.txt NOTICE.txt README.txt RELEASE-NOTES.txt TODO.JustIce
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%dir %{_javadocdir}/%{name}

%if %manual
%files manual
%defattr(0644,root,root,0755)
%doc docs/*
%endif


