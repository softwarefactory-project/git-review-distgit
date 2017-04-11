Name:		git-review
Version:	1.24
Release:	5%{?dist}
Summary:	A Git helper for integration with Gerrit

Group:		Development/Tools
License:	ASL 2.0
URL:		https://github.com/openstack-infra/git-review
Source0:	http://tarballs.openstack.org/git-review/git-review-%{version}.tar.gz
Source1:	git-review.conf
Patch1:		git-review-1.24-man.patch
Patch2:		git-review-1.24-main.patch

BuildArch:	noarch
BuildRequires:	python2-devel
BuildRequires:	python-pbr
BuildRequires:	python-setuptools

Requires:	git
Requires:	python-requests
Requires:	python-setuptools

%description
An extension for source control system Git that creates and manages review
requests in the patch management system Gerrit. It replaces the rfc.sh script.

%prep
%setup -q

%patch1 -p1
%patch2 -p1

%build
%{__python} setup.py build
sed -i 's/\r//' LICENSE

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/git-review/
cp %{SOURCE1} %{buildroot}%{_sysconfdir}/git-review/

# We do not save ".gitreview" as dot.gitreview because the man page has it too.
# cp .gitreview #{buildroot}/usr/share/doc/dot.gitreview

install -p -m 0644 -D git-review.1 %{buildroot}%{_mandir}/man1/git-review.1

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/git-review
%{_mandir}/man1/git-review.1.gz
# Our package name is git-review, but setup.py installs with underscore.
%{python_sitelib}/git_review/
%{python_sitelib}/git_review-%{version}-*.egg-info/

%dir %{_sysconfdir}/git-review/
%config(noreplace) %{_sysconfdir}/git-review/git-review.conf
# License is required in percent-doc according to Packaging:LicensingGuidelines
%doc AUTHORS LICENSE
%doc README.rst

%changelog
* Fri Apr 24 2015 Pete Zaitcev <zaitcev@redhat.com> - 1.24-5
- Add runtime requirement for setuptools to provide pkg_resources (#1214040)

* Fri Mar 06 2015 Pete Zaitcev <zaitcev@redhat.com> - 1.24-4
- Catch internal exceptions properly, avoid tripping abrtd (#1188913)
- Rebuilt for EPEL 7

* Thu Dec 11 2014 Pete Zaitcev <zaitcev@redhat.com> - 1.24-3
- Fix up the man page (#1170410)

* Tue Nov 11 2014 Pete Zaitcev <zaitcev@redhat.com> - 1.24-2
- Require python-requests (#1162709)

* Wed Oct 29 2014 Pete Zaitcev <zaitcev@redhat.com> - 1.24-1
- Upstream 1.24: better deal w/ proxies, https; bugfixes (e.g. unicode crash)
- Checking for updates is out, other configuration options are in

* Wed Sep 03 2014 Pete Zaitcev <zaitcev@redhat.com>
- 1.22-3
- Rebuilt for EPEL 7

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Aug 09 2013 Pete Zaitcev <zaitcev@redhat.com>
- 1.22-1
- Upstream 1.22: per-user configurations, tweaks to gerrit branch search

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 21 2013 Pete Zaitcev <zaitcev@redhat.com>
- 1.20-0.1
- Upstream 1.20: can have a file called "HEAD"; add -d option
- Patch the breakage with manpage in setup.py (temporarily - upstream pending)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Sep 13 2012 Pete Zaitcev <zaitcev@redhat.com>
- 1.18-1
- Upstream 1.18: list actions

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Pete Zaitcev <zaitcev@redhat.com>
- 1.17-1
- Upstream 1.17: refs/publish, no ssh -Y, adapt to newer git so -d works

* Wed Apr 11 2012 Pete Zaitcev <zaitcev@redhat.com>
- 1.16-1
- Update to upstream 1.16: supports Gerrit 2.3 API (for draft reviews e.g.).

* Tue Apr 10 2012 Pete Zaitcev <zaitcev@redhat.com>
- 1.15-1
- Update to upstream 1.15: everything except the big refactor for OSX.

* Tue Feb 7 2012 Pete Zaitcev <zaitcev@redhat.com>
- 1.12-2
- Update with Rob Kukura's review comments: drop python_sitelib etc.

* Tue Jan 31 2012 Pete Zaitcev <zaitcev@redhat.com>
- 1.12-1
- Use upstream way to disable checking for updates; no more patching

* Wed Jan 18 2012 Pete Zaitcev <zaitcev@redhat.com>
- 1.9-4
- Strip CR characters from LICENSE at build time

* Tue Jan 17 2012 Pete Zaitcev <zaitcev@redhat.com>
- 1.9-3
- Update for Fedora packaging review

* Mon Jan 9 2012 Pete Zaitcev <zaitcev@redhat.com>
- 1.9-2
- Disable checking PyPi by default, add option -P to force it.

* Wed Jan 4 2012 Pete Zaitcev <zaitcev@redhat.com>
- 1.9-1

* Fri Dec 30 2011 Pete Zaitcev <zaitcev@redhat.com>
- 1.8-1
- New upstream version
- Build from original upstream tarball, do not repack

* Sat Dec 24 2011 Pete Zaitcev <zaitcev@redhat.com>
- 1.7-1
- Initial spec for Fedora
