#
# spec file for package opencv
#
# Copyright (c) 2017 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           librealsense
Version:        2.22.0
Release:        97.5
Summary:        Library for capturing data from the Intel(R) RealSense(TM) depth cameras (D400 series and the SR300) and the T265 tracking camera.
License:        ASL-2.0
Packager:  Alessandro de Oliveira Faria (A.K.A CABELO) <cabelo@opensuse.org>
Group:          Development/Libraries/C and C++
Url:            https://software.intel.com/en-us/intel-realsense-sdk
Source0:        https://github.com/IntelRealSense/librealsense/archive/librealsense-%{version}.tar.gz
BuildRequires: -post-build-checks -rpmlint-Factory -rpmlint-mini  -rpmlint
BuildRequires:  unzip git
BuildRequires:  gcc gcc-c++ 
%if 0%{?suse_version}
BuildRequires:  cmake
BuildRequires:  udev gtk3-devel glu-devel libglfw3 libglfw-devel
BuildRequires:  libusb-1_0-devel pkg-config
%endif

%if 0%{?fedora_version}

%if 0%{?fedora_version} >26
BuildRequires:  cmake
BuildRequires:  udev gtk3-devel  glfw glfw-devel
BuildRequires:  pkgconf-pkg-config
BuildRequires:  libusb1-devel
%endif

%if 0%{?fedora_version} <27
BuildRequires:  cmake
BuildRequires:  udev gtk3-devel glfw glfw-devel
BuildRequires:  pkgconfig
BuildRequires:  libusb1-devel
%endif

%endif
%if 0%{?rhel_version} || 0%{?centos_version}
BuildRequires:  pkgconfig
BuildRequires:  udev gtk3-devel glu-devel glfw glfw-devel
BuildRequires:  libusb1-devel 
BuildRequires: cmake >= 2.8.12.2

%endif

%if 0%{?suse_version}
#Requires:      libusb-1_0
%else
Requires:      libusb1
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-build


%description
Library for capturing data from the Intel(R) RealSense(TM)  depth cameras (D400 series and the SR300) and the T265 tracking camera. This effort was initiated to better support researchers, creative coders, and app developers in domains such as robotics, virtual reality, and the internet of things. Several often-requested features of RealSense(TM); devices are implemented in this project, including multi-camera capture.

%package devel
Summary:        Development files for using the RealSense library
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}

%description devel
Devel package of the library for capturing data from the Intel(R) RealSense(TM) depth cameras (D400 series and the SR300) and the T265 tracking camera. This effort was initiated to better support researchers, creative coders, and app developers in domains such as robotics, virtual reality, and the internet of things. Several often-requested features of RealSense(TM); devices are implemented in this project, including multi-camera capture.

%prep
%setup -q -a 0

%build
export CFLAGS="%{optflags} $(getconf LFS_CFLAGS)"
export CXXFLAGS="%{optflags} ${mlra} $(getconf LFS_CFLAGS)"
mkdir build
cd build
cmake .. 
make %{?_smp_mflags} VERBOSE=0

%install
cd build
make DESTDIR=%{?buildroot:%{buildroot}} install/fast
mkdir -p %{?buildroot}/etc//udev/rules.d/
cp ../config/99-realsense-libusb.rules %{?buildroot}/etc//udev/rules.d/ 
%ifnarch x86_64
rm %{?buildroot}/usr/local/lib/cmake/realsense/realsenseConfig.cmake 
rm %{?buildroot}/usr/local/lib/cmake/realsense/realsenseTargets-noconfig.cmake
rm %{?buildroot}/usr/local/lib/cmake/realsense/realsenseTargets.cmake
%endif

#%post -n %{name} -p /sbin/ldconfig

%post 
/usr/bin/udevadm control --reload-rules
/usr/bin/udevadm trigger
/sbin/ldconfig

%postun -n %{name} -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_usr}/local/bin/*
%{_usr}/local/lib64/librealsense2-gl.so.%{version}
%{_usr}/local/lib64/librealsense2.so.%{version}
%{_usr}/local/lib64/lib*.a
%{_sysconfdir}/udev/rules.d/99-realsense-libusb.rules

%files devel
%defattr(-,root,root,-)
%{_usr}/local/lib64/librealsense2.so.2.22
%{_usr}/local/lib64/librealsense2.so
%{_usr}/local/lib64/librealsense2-gl.so.2.22
%{_usr}/local/lib64/librealsense2-gl.so
%{_usr}/local/lib64/cmake/glfw3/*
%{_usr}/local/lib64/cmake/realsense2/*
%{_usr}/local/lib64/pkgconfig/*
%{_usr}/local/include/GLFW/*
%{_usr}/local/include/librealsense2/*
%{_usr}/local/include/librealsense2/h/*
%{_usr}/local/include/librealsense2/hpp/*


%changelog
