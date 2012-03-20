from lande.utilities.jobbuilder import JobBuilder

b = JobBuilder(
    savedir='$simpsdata/v1',
    code='$simpscode/simulate.py',
    num=10)
b.build()
