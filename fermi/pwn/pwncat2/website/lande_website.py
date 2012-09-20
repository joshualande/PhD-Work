from lande.fermi.pipeline.pwncat2.website.builder import WebsiteBuilder

#builder=WebsiteBuilder(
#                     pwndata='$pwncode/data/pwncat2_data_lande.yaml',
#                     fitdir='$pwndata/spectral/v29/analysis',
#                     webdir='$pwndata/spectral/v29/website')
#builder.build()

builder=WebsiteBuilder(
                     pwndata='$pwndata/pwncat2_data_lande.yaml',
                     fitdir='$pwnpipeline/v35/analysis',
                     webdir='$pwnpipeline/v35/website')
builder.build()

