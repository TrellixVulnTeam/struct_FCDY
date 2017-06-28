Build on Linux
--------------

.. contents::
   :local:
   :depth: 1

Prerequisites
^^^^^^^^^^^^^

Our build system requires:

* Required.

  * `CMake <https://cmake.org/>`_ (>=3.1)
  * Python 2.7: Devel, PIP
  * make, gcc, g++

* Recommended.

  * CUDA Toolkit 8.0 / cuDNN 6.0 (to build CUDA/cuDNN extension for NVIDIA GPU)


Setup build environment
^^^^^^^^^^^^^^^^^^^^^^^

Install apt packages
""""""""""""""""""""

.. code-block:: shell

    sudo apt-get install -y --no-install-recommends ccache cmake curl g++ make unzip git


Install python requirements
"""""""""""""""""""""""""""

.. code-block:: shell

    sudo apt install python-dev python-pip python-setuptools python-virtualenv
    sudo pip install --upgrade pip  # bump to latest version


Install protoc
""""""""""""""

.. code-block:: shell

    curl -L https://github.com/google/protobuf/releases/download/v3.1.0/protoc-3.1.0-linux-x86_64.zip -o /tmp/protoc-3.1.0-linux-x86_64.zip
    sudo unzip -d /usr/local /tmp/protoc-3.1.0-linux-x86_64.zip && sudo chmod 755 /usr/local/bin/protoc


Install CUDA and cuDNN
""""""""""""""""""""""

- Get deb package from NVIDIA page.
 - https://developer.nvidia.com/cuda-downloads 
 - Linux -> x86_64 -> Ubuntu -> 16.04 -> deb(network)
 - https://developer.nvidia.com/rdp/cudnn-download (Register required)
 - Download cuDNN v6.0 (April 27, 2017), for CUDA 8.0 -> cuDNN v6.0 Runtime Library for Ubuntu16.04 (Deb)
 - Download cuDNN v6.0 (April 27, 2017), for CUDA 8.0 -> cuDNN v6.0 Developer Library for Ubuntu16.04 (Deb)

 - Please double check that files you downloaded are correct


.. code-block:: shell

    sudo dpkg -i /home/ubuntu/cuda-repo-ubuntu1604_8.0.61-1_amd64.deb
    sudo apt update
    sudo apt upgrade -y  # It may take long time.....
    sudo apt install -y cuda-8.0  # It may take long time.....
    sudo dpkg -i /home/ubuntu/libcudnn6_6.0.21-1+cuda8.0_amd64.deb
    sudo dpkg -i /home/ubuntu/libcudnn6-dev_6.0.21-1+cuda8.0_amd64.deb

- Please reboot your system to enable GPU driver.


Build and installation
^^^^^^^^^^^^^^^^^^^^^^

Build and install
"""""""""""""""""

.. code-block:: shell

    git clone https://github.com/sony/nnabla
    cd nnabla
    sudo pip install -U -r python/setup_requirements.txt
    sudo pip install -U -r python/requirements.txt
    mkdir build
    cd build
    cmake ../
    make -j 16
    cd dist
    sudo pip install -U nnabla-<package version>-<package-arch>.whl # a name may depend on an environment


Build and install CUDA/cuDNN extension
""""""""""""""""""""""""""""""""""""""

.. code-block:: shell

    git clone https://github.com/sony/nnabla-ext-cuda
    cd nnabla-ext-cuda
    sudo pip install -U -r python/requirements.txt
    mkdir build
    cd build
    cmake ../
    make -j 16
    cd dist
    sudo pip install -U nnabla_ext_cuda-<package version>-<package-arch>.whl


Unit test
^^^^^^^^^

For unit testing, some additional requirements should be installed.

.. code-block:: shell

    cd nnabla
    sudo pip install -U -r python/test_requirements.txt

Then run(on nnabla directory):

.. code-block:: shell

    py.test python/test

Then run CUDA/cuDNN extension(on nnabla directory):

.. code-block:: shell

    export PYTHONPATH=<your path for nnabla-ext-cuda>/python/test:$PYTHONPATH
    py.test python/test



FAQ
^^^

Q. Why do I need to reboot after installing CUDA/cuDNN?
"""""""""""""""""""""""""""""""""""""""""""""""""""""""

CUDA driver may remain disabled. Therefore, you need to reboot the system and enable the driver.

Q. I do not have the root privilege.
""""""""""""""""""""""""""""""""""""

If you do not have the root privilege, please use virtualenv.

