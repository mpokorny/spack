# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gasnetex(AutotoolsPackage):
    """GASNetEx is a language-independent, low-level networking layer
       that provides network-independent, high-performance communication
       primitives tailored for implementing parallel global address space
       SPMD languages and libraries such as UPC, Co-Array Fortran, SHMEM,
       Cray Chapel, and Titanium.
    """
    homepage = "https://gasnet.lbl.gov"
    url      = "https://gasnet.lbl.gov/EX/GASNet-2020.3.0.tar.gz"

    version('2020.3.0', sha256='019eb2d2284856e6fabe6c8c0061c874f10e95fa0265245f227fd3497f1bb274')
    version('2019.9.0', sha256='117f5fdb16e53d0fa8a47a1e28cccab1d8020ed4f6e50163d985dc90226aaa2c')
    version('2019.6.0', sha256='839ba115bfb48083c66b4c1c27703d73063b75d2f1e0501d5eab2ad7f0f776c8')
    version('2019.3.2', sha256='9e2175047879f1e8c7c4b0a9db3c2cd20c978371cd7f209cf669d402119b6fdb')
    version('2019.3.0', sha256='97fe19bb5ab32d14a96d2dd19d0f03048f68bb20ca83abe0c00cdab40e86eba5')
    version('1.32.0', sha256='42e4774b3bbc7c142f77c41b6ce86b594f579073f46c31f47f424c7e31ee1511')
    version('1.30.0', sha256='b5d8c98c53174a98a41efb4ec9dedb62c0a9e8fa111bb6460cd4493beb80d497')
    version('1.28.2', sha256='7903fd8ebdd03bcda20a66e3fcedef2f8b384324591aa91b8370f3360f6384eb')
    version('1.28.0', sha256='a7999fbaa1f220c2eb9657279c7e7cccd1b21865d5383c9a5685cfe05a0702bc')
    version('1.24.0', sha256='76b4d897d5e2261ef83d0885c192e8ac039e32cb2464f11eb64eb3f9f2df38c0')


    variant('debug', default=False, 
            description="Build in debugging mode.")
    variant('debug-malloc', default=False,
            description="Enable malloc debugging (note: enabled with 'debug')")
    variant('dev-warnings', default=False,
            description="Build with developer compiler warnings for the library and tests.")
    variant('verbose', default=False,
            description="Enable debugging status messages.")
    variant('trace', default=False,
            description="Enable tracing.")
    variant('stats', default=False,
            description="Enable gathering of statistics.")


    variant('segment-fast', default=False,
            description="Build in the FAST shared segment configuration.")
    variant('segment-large', default=False, 
            description="Build in the LARGE shared segment configuration.")
    variant('segment-everything', default=False,
            description="Build in the EVERYTHING shared segment configuration.")
    # max-segsize controls the upper limit for FAST/LARGE segment size on most conduits
    # In FAST and LARGE segment configurations, GASNet probes each compute node at
    # startup to determine an upper-limit on the available space for the segment 
    # This value provides one upper-limit to that probe, which also has the effect of 
    # limiting the space available for client segments. The parameter has the following 
    # format: size_spec ( / opt_suffix ) where 'size_spec' is either an absolute memory 
    # size: [0-9]+{KB,MB,GB}  or a fraction of compute node physical memory: 0.85
    # and 'opt_suffix' is one of the following: (or empty, which means "P") "P" : means the 
    # limit is per-process and EXCLUDES internal GASNet objects "H" : means the limit is 
    # host-wide and INCLUDES internal GASNet objects.  See the GASNet documentation for 
    # more details. 
    # 
    # Examples:
    # "0.85/H" : limit host-wide use at 85% of physical memory (this is also the default)
    # "4GB/P"  : try to ensure 4GB per process of GASNet shared segment space
    variant('max-seg-size', default="4GB", 
            description="Build-time default value for GASNET_MAX_SEGSIZE.")
    variant('aligned-segments', default=False,
            description="Force aligned for allocated segment base address.")

    # Inter-process shared memory options. 
    variant('enable-pshm', default=True, 
            description="Enable inter-process shared memory support.")
    variant('enable-pshm-xpmem', default=False, 
            description="Enable use of XPMEM for inter-process shared memory support.")
    variant('enable-pshm-hugetlbfs', default=False, 
            description="Enable use of hugetlbfs for inter-process shared memory support.")
    variant('enable-pshm-file', default=False, 
            description="Enable use of mmap()ed temporary files for inter-process shared memory support.")
    variant('enable-large-pshm', default=False, 
            description="Enable PSHM support for upto 45k cores per node (default is 255 cores).")

    # For spack we assume we always want a parallel client. 
    variant('seq-client', default=False,
            description="Enable sequential cilents.")
    variant('par-client', default=True, 
            description="Enable parallel clients.")
    variant('parsync', default=False, 
            description="Enable parsync-mode clients.")
    variant('pthreads', default=True, 
            description="Enable use of pthreads (required to support (p)threaded clients.)")
    variant('max-pthreads-per-node', values=int, default=4, # TODO: What's a good value for this?
            description="Set the maximum number of pthreads per GASNet node.")

    variant('conservative-local-copy', default=False,
            description="Enable use of conservative (slower) mechanism for local data movement.")

    variant('mpi-compat', default=False,
            description="Enable MPI compatibility for all conduits.")

    default_conduit = 'auto'
    if (spack.architecture.platform().name == 'cray'):
        default_conduit='aires'
    variant("conduit", default=default_conduit,
            values=("smp", "udp", "mpi", "ucx", "aries", "ibv", "auto"),
            description="The transport conduit to use.", 
            multi=True)

    # IBV conduit specific settings... 
    variant('enable-ibv-rcv-thread', default=True,
            description="Spawn an extra thread that remains blocked until the arrival of an active message.")
    variant('enable-ibv-conn-thread', default=True,
            description="Spawn an extra that remains blocked until the arrival of a connection request.")
    variant('with-ibv-spawner', default='mpi', 
            values=("mpi", "pmi", "ssh"), 
            description="The default job spawner to be used by the gasnetrun_ibv utility.", 
            multi=False)
    variant('enable-ibv-multirail', default=False,
            description="Enable support for IBV on multiple rails/hcas.")
    variant('ibv-max-hcas', values=int, default=3, 
            description='Number of HCAS for ibv configuration.',)

    # This option is really only helpful if you are building Legion.  Most users
    # should ignore it... 
    variant('legion', default=False, 
            description='Configure GASNetEx with Legion-centric build parameters.')

    # Aries conduit specific settings... 
    variant('aries-max-medium', values=int, default=4032, 
            description='specify gasnet_AMMaxMedium() for Aries interconnect.')

    conflicts('+seq-client', when='+par-client', 
              msg='Manually disable the parallel client (-par-client) to build sequential client support.')

    conflicts('+max-pthreads-per-node', when="-pthreads", 
             msg='pthreads must be enabled with +pthreads')

    conflicts('+segment-fast', when='+segment-large', 
              msg='Conflicting shared segment configurations (only choose one)')
    conflicts('+segment-fast',  when='+segment-everything',
              msg='Conflicting shared segment configurations (only choose one)')
    conflicts('+segment-large', when='+segment-everything',
              msg='Conflicting shared segment configurations (only choose one)')


    conflicts('+enable-pshm-xpmem', when='-enable-pshm', 
              msg='interprocess shared memory support must be enabled to use pshm-xpmem')
    conflicts('+enable-pshm-hugetlbfs', when='-enable-pshm', 
              msg='interprocess shared memory support must be enabled to use pshm-hugetlbfs')
    conflicts('+enable-pshm-file', when='-enable-pshm', 
              msg='interprocess shared memory support must be enabled to use pshm-file')
    conflicts('+enable-large-pshm', when='-enable-pshm', 
              msg='interprocess shared memory support must be enabled to use large-pshm')
    conflicts('+aligned-segments', when='+enable-pshm',  # TODO: also won't work on hetrogeneous clusters. 
              msg='forced alignment not supported when interprocess shared memory is enabled.')

    # TODO: Ideally we'd raise a conflict if the conduit != ibv...  but inequality doesn't isn't supported w/ 'when'.
    # Currently we ignore these parameters in all but the ibv case below to work around this... 
    conflicts('+ibv-max-hcas', when='-enable-ibv-multirail', 
              msg='Multi-rails/-hcas requires +enable-ibv-multirail.')

    depends_on('mpi', when='conduit=mpi')
    depends_on('ucx', when='conduit=ucx')

    def url_for_version(self, version):
        url = "https://gasnet.lbl.gov/"
        if version >= Version('2019'):
            url += "EX/GASNet-{0}.tar.gz".format(version)
        else:
            url += "download/GASNet-{0}.tar.gz".format(version)

        return url

    def configure_args(self):

        args = [
            '--with-max-segsize=%s'   # note: mmap segsize has been deprecated
            % (self.spec.variants['max-seg-size'].value),
            # for shared libs
            "CC=%s %s" % (spack_cc, self.compiler.cc_pic_flag),
            "CXX=%s %s" % (spack_cxx, self.compiler.cxx_pic_flag),
        ]

        if '+debug' in self.spec:
            # default is disabled. 
            args.append('--enable-debug')
        if '+debug-malloc' in self.spec:
            # default is disabled. 
            args.append('--enable-debug-malloc')
        if '+dev-warnings' in self.spec:
            # default in gasnet's config is enabled. 
            args.append('--enable-dev-warnings')
        else:
            args.append('--disable-dev-warnings')
        if '+verbose' in self.spec:
            # default is disabled. 
            args.append('--enable-gasnet-verbose')
        if '+trace' in self.spec:
            # default is disabled. 
            args.append('--enable-trace')
        if '+stats' in self.spec:
            # default is disabled. 
            args.append('--enable-stats')

        # Memory segment configuration...  
        if '+segment-fast' in self.spec:
            args.append('--enable-segment-fast')
        if '+segment-large' in self.spec:
            args.append('--enable-segment-large')
        if '+segment-everything' in self.spec:
            args.append('--enable-segment-everything')
        if '+aligned-segments' in self.spec:
            args.append('--enable-aligned-segments')
        # Note that max segment size is handled in the initial args set.


        # Inter-process shared memory support flags. 
        if '+enable-pshm' in self.spec:
            args.append('--enable-pshm')
        else:
            args.append('--disable-pshm')
        if '+enable-pshm-xpmem' in self.spec:
            # default is disabled. 
            args.append('--enable-pshm-xpmem')
        if '+enable-pshm-hugetlbfs' in self.spec:
            # default is disabled.
            args.append('--enable-pshm-hugetlbfs')
        if '+enable-pshm-file' in self.spec:
            # default is disabled.
            args.append('--enable-pshm-file')
        if '+enable-large-pshm' in self.spec:
            args.append('--enable-large-pshm')

        # Parallel or sequential client configuration.
        if '+seq-client' in self.spec:
            args.append('--enable-seq')
        else:
            args.append('--disable-seq')
        if '+par-client' in self.spec:
            args.append('--enable-par')
        else:
            args.append('--disable-par')
        if '+parsync' in self.spec:
            args.append('--enable-parsync')
        else:
            args.append('--disable-parsync')


        if '+pthreads' in self.spec:
            args.append('--enable-pthreads')
        else:
            args.append('--disable-pthreads')

        if '+max-pthreads-per-node' in self.spec:
            args.append('--with-max_pthreads_per_node={%d}' % 
                self.spec.variants['max-pthreads-per-node'].value)

        # MPI compatibility. 
        if '+mpi-compat' in self.spec:
            args.append('--enable-mpi-compat')
        else:
            args.append('--disable-mpi-compat')

        if '+conservative-local-copy' in self.spec:
            # default is disabled. 
            args.append('--enable-conservative-local-copy')

        if 'conduit=auto' in self.spec:
            # this is the default -- we let 'auto' override 
            # all other conduit options. 
            args.append('--enable-auto-conduit-detect')
        else:
            # we have one or more conduit options to 
            # consider.  With any specific conduits 
            # listed we disable 'auto'...
            args.append('--disable-auto-conduit-detect')

            conduits = list(self.spec.variants['conduit'].value)
            for c in conduits:
                conduit_arg=''.join('--enable-{0}'.format(c))
                args.append(conduit_arg)

                if c == 'ibv':
                    if '+enable-ibv-multirail' in self.spec:
                        args.append('--enable-ibv-multirail')
                    if '+with-ibv-max-hcas' in self.spec:
                        args.append('--with-ibv-max_hcas=%d' % 
                            (self.spec['with-ibv-max-hcas'].value))
                elif c == 'aries':
                    if '+aries-max-medium' in self.spec:
                        args.append('--with-aries-max-medium=%d' % 
                            (self.spec['aries-max-medium'].value))


        if '+legion' in self.spec:
            # notes: we leave conduit specification to the normal path here.
            args.extend(['--disable-portals',
                         '--disable-mxm',
                         '--enable-pthreads',
                         '--enable-segment-fast',
                         '--enable-par', 
                         '--disable-seq',
                         '--disable-parsync',
                         '--disable-pshm',
                         '--disable-fca',
                         '--disable-aligned-segments']
                        )
            conduits = list(self.spec.variants['conduit'].value)
            if 'ibv' in conduits: 
                args.extend(['--with-ibv-spawner=mpi',
                            '--disable-ibv-rcv-thread'])
            # TODO: need to sort out cray-centric behaviors here...

        return args