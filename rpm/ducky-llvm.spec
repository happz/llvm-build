%global llvm_commit 0a5b999bcbc3d8d6a0d4ca4bff12f3685f78db52
%global clang_commit 2aa0aa926f3ed639f5041d5dc716cba5abee5035
%global lld_commit ca81503b8145e715758ed9dfff142b939a93018b

# disable debug package, otherwise error: Empty %files file …/debugfiles.list
%define debug_package %{nil}

Name:		ducky-llvm
Version:	7.0.0
Release:	8%{?dist}
Summary:	The Low Level Virtual Machine build for Ducky VM

License:	NCSA
URL:      https://github.com/happz/llvm
Source0:  https://github.com/happz/ducky-llvm/archive/%{llvm_commit}/ducky-llvm-%{llvm_commit}.tar.gz
Source1:  https://github.com/happz/ducky-clang/archive/%{clang_commit}/ducky-clang-%{clang_commit}.tar.gz
Source2:  https://github.com/happz/ducky-lld/archive/%{lld_commit}/ducky-lld-%{lld_commit}.tar.gz

BuildRequires:  ninja-build
BuildRequires:	cmake
BuildRequires:	cmake-data
BuildRequires:  make

%description
LLVM is a compiler infrastructure designed for compile-time, link-time,
runtime, and idle-time optimization of programs from arbitrary programming
languages. The compiler infrastructure includes mirror sets of programming
tools as well as libraries with equivalent functionality.

This build of LLVM is patched to produce assembly code for Ducky VM.

%prep
%autosetup -n ducky-llvm-%{llvm_commit}
mkdir -p tools/clang
tar xzf %{_sourcedir}/ducky-clang-%{clang_commit}.tar.gz -C tools/clang --strip 1
mkdir -p tools/lld
tar xzf %{_sourcedir}/ducky-lld-%{lld_commit}.tar.gz -C tools/lld --strip 1

%build
mkdir -p _build
cd _build

cmake .. -DCMAKE_BUILD_TYPE=Release \
         -DLLVM_ENABLE_ASSERTIONS=Off \
         -DLLVM_BUILD_TESTS=OFF \
         -DLLVM_BUILD_DOCS=OFF \
         -DLLVM_OPTIMIZED_TABLEGEN=ON \
         -DLLVM_TARGETS_TO_BUILD=Ducky \
         -DLLVM_DEFAULT_TARGET_TRIPLE=ducky-none-none \
         -DCLANG_VENDOR=happz/ducky \
         -DCMAKE_INSTALL_PREFIX=%{buildroot}/opt/ducky
cmake --build .

%install
cd _build
# make install DESTDIR=%{buildroot} -C _build
cmake --build . --target install

%files
/opt/ducky/bin/*
/opt/ducky/include/*
/opt/ducky/lib/*
/opt/ducky/libexec/*
/opt/ducky/share/*

%changelog
