from Utilities_spf import *
update_super_file("Super_File_test_pulsar.yaml","Super_File_at_tev.yaml","/afs/slac/g/glast/users/rousseau/TeV_sources/runs/04_04_10deg/",hypothesis="at_tev")
plot_seds("Super_File_at_tev.yaml",output="plots_at_tev",pulsars=True)
update_super_file("Super_File_test_pulsar.yaml","Super_File_point.yaml","/afs/slac/g/glast/users/rousseau/TeV_sources/runs/04_04_10deg/",hypothesis="point")
plot_seds("Super_File_point.yaml",output="plots_point",pulsars=True)
update_super_file("Super_File_test_pulsar.yaml","Super_File_extended.yaml","/afs/slac/g/glast/users/rousseau/TeV_sources/runs/04_04_10deg/",hypothesis="extended")
plot_seds("Super_File_extended.yaml",output="plots_extended",pulsars=True)
