#exit 1
for type in FileFunction LogParabola; do
    for i in `seq 0 0`; do
        istr=`printf %05d $i`
        folder=${type}_simulation/$istr/
        mkdir -p $folder
        sub="python $PWD/simulate.py $i --spectrum $type"
        echo $sub
        bsub -q xxl -oo $folder/log_$type.txt $sub
    done
done
