# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Flexflow(CMakePackage):
    """FlexFlow is a deep learning framework that accelerates distributed DNN 
    training by automatically discovering fast parallelization strategies.
    """
    homepage = "http://legion.stanford.edu/"
    git      = "https://github.com/flexflow/FlexFlow.git"


    variant('build-alexnet', Default=False,
            description="Build the Alexnet example.")
    variant('build-alexnet-newapi', Defualt=False,
            description="Build the Alexnet example using the new API.")
    variant('build-all-examples', Default=False,
            description="Build all of the example networks.")
    variant('build-candle-uno', Default=False,
            description="Build the CANDLE UNO example network.")
    variant('build-dlrm', Default=False,
            description="Build the DLRM example network.")
    variant('build-inception', Default=False, 
            description="Build the Inception example network.")
    variant('build-poca')

    depends_on('legion@stable+cuda+cuda-hijack')
    depends_on('protobuf@3.12:')
    depends_on('nccl@2.7:', when="+nccl")

    def cmake_args(self):

        if '+build-all-examples' in self.spec:
            options.append('-DBUILD_ALL_EXAMPLES=ON')
        else:
            options.append('-DBUILD_ALL_EXAMPLES=OFF')

        if '+build-alexnet' in self.spec:
            options.append('-DBUILD_ALEXNET=ON')
        else:
            options.append('-DBUILD_ALEXNET=OFF')
        if '+build-alexnet-newapi' in self.spec:
            options.append('-DBUILD_ALEXNET_NEWAPI=ON')
        else:
            options.append('-DBUILD_ALEXNET_NEWAPI=OFF')
        if '+build-alexnet-newapi' in self.spec:
            options.append('-DBUILD_ALEXNET_NEWAPI=ON')
        else:
            options.append('-DBUILD_ALEXNET_NEWAPI=OFF')    

        return options
