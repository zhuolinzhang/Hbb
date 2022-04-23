fileList=`ls ratio_*_[0-9].pdf`
for file in $fileList
do
	cp $file "chap6_$file"
done