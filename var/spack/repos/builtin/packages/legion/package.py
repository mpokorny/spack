# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Legion(CMakePackage):
    """Legion is a data-centric parallel programming system for writing
       portable high performance programs targeted at distributed heterogeneous
       architectures. Legion presents abstractions which allow programmers to
       describe properties of program data (e.g. independence, locality). By
       making the Legion programming system aware of the structure of program
       data, it can automate many of the tedious tasks programmers currently
       face, including correctly extracting task- and data-level parallelism
       and moving data around complex memory hierarchies. A novel mapping
       interface provides explicit programmer controlled placement of data in
       the memory hierarchy and assignment of tasks to processors in a way
       that is orthogonal to correctness, thereby enabling easy porting and
       tuning of Legion applications to new architectures.
    """
    homepage = "http://legion.stanford.edu/"
    url      = "https://github.com/StanfordLegion/legion/tarball/legion-20.06.0"
    git      = "https://github.com/StanfordLegion/legion.git"

    version('master', branch='master')
    version('stable',  branch='stable')
    version('20.06.0', tag='legion-20.06.0')
    version('20.03.0', tag='legion-20.03.0')
    version('19.12.0', tag='legion-19.12.0')
    version('19.09.1', tag='legion-19.09.1')
    version('19.09.0', tag='legion-19.09.0')
    version('19.06.0', tag='legion-19.06.0')
    version('19.04.0', tag='legion-19.04.0')
    version('18.12.0', tag='legion-18.12.0')
    version('18.09.0', tag='legion-18.09.0')
    version('18.02.0', tag='legion-18.02.0')
    version('ctrl-rep', branch='control_replication')

    variant('shared-libs', default=False,
            description="Build shared libraries.")

    variant('network', default='none', 
            values=("gasnetex", "mpi", "none"), 
            description="The network communications layer to use.", 
            multi=False)

    variant('bounds-checks', default=False,
            description="Enable bounds checking in Legion accessors.")
    variant('privilege-checks', default=False, 
            description="Enable runtime privildge checks in Legion accessors.")
    variant('enable-tls', default=False, 
            description="Enable thread-local-storage of the Legion context.")
    variant('output-level', default='warning',
            # Note: values are dependent upon Legion's cmake parameters...
            values=("spew", "debug", "info", "print", "warning", "error", "fatal", "none"),
            description="Set the compile-time logging level.", 
            multi=False)
    variant('spy', default=False, 
            description="Enable detailed logging for Legion Spy debugging.")

    variant('cuda', default=False, 
            description="Enable CUDA support.")
    variant('cuda-hijack', default=False,
            description="Hijack application calls into the CUDA runtime (implies +cuda).")
    # note on arch values: 60=pascal, 70=volta, 75=turing 
    variant('cuda-arch', default='70', # default to supporting volta
            values=("60", "70", "75"), 
            description="GPU/CUDA architecture to build for.", 
            multi=True)
    variant('fortran', default=False, 
            description="Enable Fortran bindings.")
    variant('hdf5', default=False,
            description="Enable support for HDF5.")
    variant('hwloc', default=False,
            description="Use hwloc for topology awareness.")
    variant('kokkos', default=False,
            description="Enable support for interoperability with Kokkos.")
    variant('libdl', default=True, 
            description="Enable support for dynamic loading (via libdl).")
    variant('llvm', default=False,
            description="Enable support for LLVM IR JIT  within the Realm runtime.")
    variant('link-llvm-libs', default=False,
            description="Link LLVM libraries into the Realm runtime library.")
    variant('openmp', default=False,
            description="Enable support for OpenMP within Legion tasks.")
    variant('papi', default=False, 
            description="Enable PAPI performance measurements.")
    variant('python', default=False, 
            description="Enable Python support.")
    variant('zlib', default=True, 
            description="Enable zlib support.")
    
    variant('redop-complex', default=False,
            description="Use reduction operators for complex types.")
    
    variant('build-all', default=False, 
            description="Build everything: all bindings, examples, tutorials, tests, apps, etc.")
    variant('build-apps', default=False, 
            description="Build the sample applicaitons.")
    variant('build-bindings', default=False, 
            description="Build all the language bindings (C, Fortran, Python, etc.).")
    variant('build-examples', default=False, 
            description="Build the (small'ish) examples.")
    variant('build-tests', default=False, 
            description="Build the test suite.")
    variant('build-tutorial', default=False, 
            description="Build the Legion tutorial examples.")
    

    variant('max-dims', values=int, default=3, 
            description="Set the maximum number of dimensions available in a logical region.")
    variant('max-fields', values=int, default=512,
            description="Maximum number of fields allowed in a logical region.")

    conflicts('+cuda-hijack', when='-cuda')

    depends_on("cmake@3.1:", type='build')
    depends_on('mpi', when='network=mpi')
    depends_on('gasnetex', when='network=gasnetex')
    depends_on('hdf5', when='+hdf5')
    depends_on('llvm@7.1.0', when='+llvm')
    depends_on('llvm@7.1.0', when='+link-llvm-libs')
    depends_on('cuda@10:', when='+cuda')
    depends_on('hdf5', when='+hdf5')
    depends_on('zlib@1.2.11', when="zlib")

    def cmake_args(self):
        cmake_cxx_flags = [ ]
        options = [ ]
        if '+shared_libs' in self.spec:
            options.append('-DBUILD_SHARED_LIBS=ON')
        else:
            options.append('-DBUILD_SHARED_LIBS=OFF')

        if '+bounds_checks' in self.spec:
            # default is off. 
            options.append('-DLegion_BOUNDS_CHECKS=ON')
        if '+privilege_checks' in self.spec:
            # default is off. 
            options.append('-DLegion_PRIVILEGE_CHECKS=ON')
        if '+enable-tls' in self.spec:
            # default is off. 
            options.append('-DLegion_ENABLE_TLS=ON')
        if 'output-level' in self.spec:
            level = str.upper(self.spec.variants['output-level'].value)
            options.append('-DLegion_OUTPUT_LEVEL=%s' % level)
        if '+spy' in self.spec:
            # default is off. 
            options.append('-DLegion_SPY=ON')
  
        if 'network=gasnet' in self.spec:
            options.append('-DLegion_NETWORKS=gasnet1')
        elif 'network=mpi' in self.spec: 
            options.append('-DLegion_NETWORKS=mpi')
        # else is no-op... 
        
        if '+cuda' in self.spec:
            cuda_arch = list(self.spec.variants['cuda-arch'].value)
            arch_str = ','.join(cuda_arch)
            options.append('-DLegion_USE_CUDA=ON')
            options.append('-DLegion_GPU_REDUCTIONS=ON')
            options.append('-DLegion_CUDA_ARCH=%s' % arch_str)
            if '+cuda-hijack' in self.spec:
                options.append('-DLegion_HIJACK_CUDART=ON')
            else:
                options.append('-DLegion_HIJACK_CUDART=OFF')
        
        if '+fortran' in self.spec:
            # default is off. 
            options.append('-DLegion_USE_Fortran=ON')

        if '+hdf5' in self.spec:
            # default is off.
            options.append('-DLegion_USE_HDF5=ON')

        if '+hwloc' in self.spec:
            # default is off. 
            options.append('-DLegion_USE_HWLOC=ON')

        if '+kokkos' in self.spec:
            # default is off. 
            options.append('-DLegion_USE_Kokkos=ON')

        if '+libdl' in self.spec:
            # default is on.
            options.append('-DLegion_USE_LIBDL=ON')
        else:
            options.append('-DLegion_USE_LIBDL=OFF')
        
        if '+llvm' in self.spec:
            # default is off.
            options.append('-DLegion_USE_LLVM=ON')
        if '+link-llvm-libs' in self.spec:
            options.append('-DLegion_LINK_LLVM_LIBS=ON')
            # TODO: What do we want to do w/ this option?
            options.append('-DLegion_ALLOW_MISSING_LLVM_LIBS=OFF')

        if '+openmp' in self.spec:
            # default is off.
            options.append('-DLegion_USE_OpenMP=ON')

        if '+papi' in self.spec:
            # default is off. 
            options.append('-DLegion_USE_PAPI=ON')

        if '+python' in self.spec:
            # default is off. 
            options.append('-DLegion_USE_Python=ON')

        if '+zlib' in self.spec:
            # default is on. 
            options.append('-DLegion_USE_ZLIB=ON')
        else:
            options.append('-DLegion_USE_ZLIB=OFF')

        
        if '+redop-complex' in self.spec:
            # default is off. 
            options.append('-DLegion_REDOP_COMPLEX=ON')


        if '+build_all' in self.spec:
            # default is off. 
            options.append('-DLegion_BUILD_ALL=ON')
        if '+build-apps' in self.spec:
            # default is off. 
            options.append('-DLegion_BUILD_APPS=ON')
        if '+build-bindings' in self.spec:
            # default is off. 
            options.append('-DLegion_BUILD_BINDINGS=ON')
        if '+build-examples' in self.spec:
            options.append('-DLegion_BUILD_EXAMPLES=ON')
        if '+build-tests' in self.spec:
            options.append('-DLegion_BUILD_TESTS=ON')
        if '+build-tutorial' in self.spec:
            options.append('-DLegion_BUILD_TUTORIAL=ON')

        if self.spec.variants['build_type'].value == 'Debug':
            cmake_cxx_flags.extend([
                '-DDEBUG_REALM',
                '-DDEBUG_LEGION',
                '-ggdb',
            ])

        if '+max-dims' in self.spec:
            maxdim = self.spec.variants['max-dims'].value
            options.append('-DLegion_MAX_DIM=%d' % maxdim)
        
        if '+max-fields' in self.spec:
            maxfields = self.spec.variants['max-fields'].value
            option.append('-DLegion_MAX_FIELDS=%d' % maxfields)

        options.append('-DCMAKE_CXX_FLAGS=%s' % (" ".join(cmake_cxx_flags)))

        return options
