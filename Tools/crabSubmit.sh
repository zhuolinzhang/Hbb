dir=.
filelist=$(ls $dir | grep "crabConfig_*")

for file in $filelist
do
    crab submit $file
done