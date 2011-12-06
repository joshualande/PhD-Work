

# acroread -toPostScript has best
# performance with bounding boxes.
for i in *pdf; do
    base=`basename $i .pdf`
    acroread -toPostScript $base.pdf 
    ps2epsi $base.ps $base.eps
    rm $base.ps
done
