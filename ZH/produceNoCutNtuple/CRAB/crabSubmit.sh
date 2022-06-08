source /cvmfs/cms.cern.ch/common/crab-setup.sh
dir=.
filelist=$(ls $dir | grep "crabConfig_ZH2017_*")

for file in $filelist
do
    python $file
done
