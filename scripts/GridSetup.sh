#! /bin/bash

setupATLAS
cd source
lsetup "asetup AnalysisBase,22.2.73" panda # used for PAV2
voms-proxy-init -voms atlas 
cd ../build
cmake ../source
make
source */setup.sh
cd ..
