from lande.fermi.pipeline.gamma_quiet_psrs.website.builder import WebsiteBuilder

b=WebsiteBuilder(
    gamma_quiet_psrs_data='$gamma_quiet_psrs_data/gamma_quiet_psrs_data.yaml',
    analysisdir='$gamma_quiet_psrs_analysis/v1',
    webdir='$gamma_quiet_psrs_analysis/v1/website')
#b.build_main()
b.build_all_psrs()

