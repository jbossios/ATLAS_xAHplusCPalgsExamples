setupATLAS
cd source/
asetup AnalysisBase,master,latest
cd ../build
cmake ../source
make -j3
source */setup.sh
cd ../
