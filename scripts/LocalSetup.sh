setupATLAS
cd source/
asetup AnalysisBase,22.2.73
cd ../build
cmake ../source
make -j3
source */setup.sh
cd ../
