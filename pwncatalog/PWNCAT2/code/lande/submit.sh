

echo python loop_pwn.py -c thierry_profile.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT1/fits/thierry_profile_v2/fits



echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT1/fits/analyze_v25/analysis \
        --emin=1e2 --emax=1e5 --no-plots --no-gtlike --no-cutoff

echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT1/fits/analyze_v26/analysis 

echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT1/fits/analyze_v27/analysis  --emin 1e4 --emax 1e5 --no-plots --no-upper-limit --no-cutoff

echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT1/fits/analyze_v28/analysis  --emin 1e4 --emax 1e5 --no-plots --no-upper-limit --no-cutoff

echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT1/fits/analyze_v29/analysis 

echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT1/fits/analyze_v30/analysis  --no-plots


echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT1/fits/analyze_v31/analysis  --no-plots --emin 1e2 --emax 1e5 --binsperdec 4

echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT1/fits/analyze_v32/analysis  --no-plots 


echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT1/fits/analyze_v33/analysis  --no-plots  --emin=1e4 --emax=1e5 --binsperdec=2 

echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT1/fits/analyze_v34/analysis   --no-plots

echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT1/fits/analyze_v35/analysis  

echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT1/fits/analyze_v36/analysis   --no-plots

echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT1/fits/analyze_v37/analysis   

echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT1/fits/analyze_v38/analysis   

echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat2_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat2_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analysis/analysis_v1/analysis

echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat2_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat2_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analysis/analysis_v2/analysis --max-free=2

echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT1/fits/analyze_v39/analysis   


echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT1/fits/analyze_v40/analysis --no-at-pulsar --no-point

echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT1/fits/analyze_v41/analysis --no-at-pulsar --no-point --no-plots

echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT1/fits/analyze_v42/analysis --no-at-pulsar --no-point --no-plots --max-free=2


echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT1/fits/analyze_v43/analysis --no-at-pulsar --no-point --no-plots --max-free=2

echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT1/fits/analyze_v44/analysis

echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT1/fits/analyze_v45/analysis --no-plots

echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat2_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat2_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analysis/analysis_v3/analysis 



echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT1/fits/analyze_v46/analysis --max-free=5

echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat1_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT1/fits/analyze_v47/analysis --max-free=5 --no-plots

echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat2_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat2_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analysis/analysis_v4/analysis  --max-free=5 --no-point --no-extended

echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat2_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat2_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analysis/analysis_v5/analysis  --max-free=5 

echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat2_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat2_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analysis/analysis_v6/analysis  --max-free=5 --no-plots


echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat2_data.yaml \
        --no-phase-cut \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/high_energy/analysis_v2/analysis  \
        --emin=31622.77660168379 --emax=316227.7660168379 --no-cutoff


echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat2_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat2_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analysis/analysis_v7/analysis  --max-free=5 --no-plots

# ~ nov 30, 2011
echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat2_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat2_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analysis/analysis_v8/analysis  --max-free=5 --no-plots

echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat2_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat2_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analysis/analysis_v9/analysis  


# testing out extension fitting bugs
echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat2_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat2_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analysis/analysis_v10/analysis  --max-free=5 --no-plots --no-at-pulsar --no-point

# Try again w/ bug fix dec 4
echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat2_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat2_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analysis/analysis_v11/analysis  --max-free=5 --no-plots

echo python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat2_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat2_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analysis/analysis_v12/analysis  


# Try to study TeV PWN
echo python loop_pwn.py -c analyze_tev.py \
        --tevdata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/tevdata.yaml \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analyze_tev/v1/analysis  

# Try again w/ bug fix dec 4
echo python loop_pwn.py -c analyze_psr.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat2_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat2_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analyze_psr/v1/analysis  --max-free=5 --no-plots

echo python loop_pwn.py -c analyze_psr.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat2_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat2_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analyze_psr/v2/analysis  

# ----------------------------------------------------------------------------------------------------

echo python loop_pwn.py -c analyze_tev.py \
        --tevsources /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/tevsources.yaml \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analyze_tev/v2/analysis  

echo python loop_pwn.py -c analyze_tev.py \
        --tevsources /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/tevsources.yaml \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analyze_tev/v3/analysis  

# ----------------------------------------------------------------------------------------------------

echo python loop_pwn.py -c analyze_tev.py \
        --tevsources /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/tevsources.yaml \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analyze_tev/v4/analysis_no_plots   --no-plots
echo python loop_pwn.py -c analyze_tev.py \
        --tevsources /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/tevsources.yaml \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analyze_tev/v4/analysis_plots 


# ----------------------------------------------------------------------------------------------------

echo python loop_pwn.py -c analyze_tev.py \
        --tevsources /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/tevsources.yaml \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analyze_tev/v5/analysis_no_plots   --no-plots
echo python loop_pwn.py -c analyze_tev.py \
        --tevsources /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/tevsources.yaml \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analyze_tev/v5/analysis_plots 

# ----------------------------------------------------------------------------------------------------

echo python loop_pwn.py -c analyze_psr.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat2_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat2_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analyze_psr/v3/analysis_no_plots --no-plots

echo python loop_pwn.py -c analyze_psr.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat2_data.yaml \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/PWNCAT2/v1/pwndata/pwncat2_phase.yaml  \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analyze_psr/v3/analysis_plots

# ----------------------------------------------------------------------------------------------------

echo python loop_pwn.py -c analyze_psr.py \
        --pwndata $PWD/pwndata/pwncat2_data.yaml \
        --pwnphase $PWD/pwndata/pwncat2_phase.yaml  \
        --modify $PWD/modify/modify_psr_lande.py \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analyze_psr/v4/analysis_no_plots --no-plots

echo python loop_pwn.py -c analyze_psr.py \
        --pwndata $PWD/pwndata/pwncat2_data.yaml \
        --pwnphase $PWD/pwndata/pwncat2_phase.yaml  \
        --modify $PWD/modify/modify_psr_lande.py \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analyze_psr/v4/analysis_plots


# ----------------------------------------------------------------------------------------------------

echo python loop_pwn.py -c analyze_psr.py \
        --pwndata $PWD/pwndata/pwncat2_data.yaml \
        --pwnphase $PWD/pwndata/pwncat2_phase.yaml  \
        --modify $PWD/modify/modify_psr_lande.py \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analyze_psr/v5/analysis_no_plots --no-plots

echo python loop_pwn.py -c analyze_psr.py \
        --pwndata $PWD/pwndata/pwncat2_data.yaml \
        --pwnphase $PWD/pwndata/pwncat2_phase.yaml  \
        --modify $PWD/modify/modify_psr_lande.py \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analyze_psr/v5/analysis_plots

# ----------------------------------------------------------------------------------------------------

echo python loop_pwn.py -c analyze_psr.py \
        --pwndata $PWD/pwndata/pwncat2_data_lande.yaml \
        --pwnphase $PWD/pwndata/pwncat2_phase_lande.yaml  \
        --modify $PWD/modify/modify_psr_lande.py \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analyze_psr/v6/analysis_no_plots --no-plots

echo python loop_pwn.py -c analyze_psr.py \
        --pwndata $PWD/pwndata/pwncat2_data_lande.yaml \
        --pwnphase $PWD/pwndata/pwncat2_phase_lande.yaml  \
        --modify $PWD/modify/modify_psr_lande.py \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analyze_psr/v6/analysis_plots

# ----------------------------------------------------------------------------------------------------

echo python loop_pwn.py -c analyze_psr.py \
        --pwndata $PWD/pwndata/pwncat2_data_lande.yaml \
        --pwnphase $PWD/pwndata/pwncat2_phase_lande.yaml  \
        --modify $PWD/modify/modify_psr_lande.py \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analyze_psr/v7/analysis_no_plots --no-plots

echo python loop_pwn.py -c analyze_psr.py \
        --pwndata $PWD/pwndata/pwncat2_data_lande.yaml \
        --pwnphase $PWD/pwndata/pwncat2_phase_lande.yaml  \
        --modify $PWD/modify/modify_psr_lande.py \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analyze_psr/v7/analysis_plots

# ----------------------------------------------------------------------------------------------------

echo python $pwncode/loop_pwn.py -c $pwncode/analyze_psr.py \
        --pwndata $pwncode/pwndata/pwncat2_data_lande.yaml \
        --pwnphase $pwncode/pwndata/pwncat2_phase_lande.yaml  \
        --modify $pwncode/modify/modify_psr_lande.py \
        -o $pwndata/spectral/v8/analysis_no_plots --no-plots --max-free 5

echo python $pwncode/loop_pwn.py -c $pwncode/analyze_psr.py \
        --pwndata $pwncode/pwndata/pwncat2_data_lande.yaml \
        --pwnphase $pwncode/pwndata/pwncat2_phase_lande.yaml  \
        --modify $pwncode/modify/modify_psr_lande.py \
        -o $pwndata/spectral/v8/analysis_plots --max-free 5

# ----------------------------------------------------------------------------------------------------

echo python $pwncode/loop_pwn.py \
        -c $pwncode/analyze_psr.py \
        --pwndata $pwncode/pwndata/pwncat2_data_lande.yaml \
        --pwnphase $pwncode/pwndata/pwncat2_phase_lande.yaml  \
        --modify $pwncode/modify/modify_psr_lande.py \
        -o $pwndata/spectral/v9/analysis_no_plots --no-plots --max-free 5

echo python $pwncode/loop_pwn.py \
        -c $pwncode/analyze_psr.py \
        --pwndata $pwncode/pwndata/pwncat2_data_lande.yaml \
        --pwnphase $pwncode/pwndata/pwncat2_phase_lande.yaml  \
        --modify $pwncode/modify/modify_psr_lande.py \
        -o $pwndata/spectral/v9/analysis_plots --max-free 5

# ----------------------------------------------------------------------------------------------------

echo python $pwncode/loop_pwn.py \
        --pwndata $pwncode/pwndata/pwncat2_data_lande.yaml \
        -c $pwncode/lande/variability/test_variability.py \
        --analysis-dir $pwndata/spectral/v9/analysis_no_plots \
        -o $pwndata/spectral/v9/variability/v2

# ----------------------------------------------------------------------------------------------------

echo python $pwncode/loop_pwn.py \
        --pwndata $pwncode/pwndata/pwncat2_data_lande.yaml \
        -c $pwncode/lande/variability/test_variability.py \
        --analysis-dir $pwndata/spectral/v9/analysis_no_plots \
        -o $pwndata/spectral/v9/variability/v3

# ----------------------------------------------------------------------------------------------------

echo python $pwncode/loop_pwn.py \
        --pwndata $pwncode/pwndata/pwncat2_data_lande.yaml \
        -c $pwncode/lande/variability/test_variability.py \
        --analysis-dir $pwndata/spectral/v9/analysis_no_plots \
        -o $pwndata/spectral/v9/variability/v4

# ----------------------------------------------------------------------------------------------------

echo python $pwncode/loop_pwn.py \
        -c $pwncode/analyze_psr.py \
        --pwndata $pwncode/pwndata/pwncat2_data_lande.yaml \
        --pwnphase $pwncode/pwndata/pwncat2_phase_lande.yaml  \
        --modify $pwncode/modify/modify_psr_lande.py \
        -o $pwndata/spectral/v10/analysis_no_plots --no-plots --max-free 5

echo python $pwncode/loop_pwn.py \
        -c $pwncode/analyze_psr.py \
        --pwndata $pwncode/pwndata/pwncat2_data_lande.yaml \
        --pwnphase $pwncode/pwndata/pwncat2_phase_lande.yaml  \
        --modify $pwncode/modify/modify_psr_lande.py \
        -o $pwndata/spectral/v10/analysis_plots --max-free 5

# ----------------------------------------------------------------------------------------------------


echo python $pwncode/loop_pwn.py \
        -c $pwncode/analyze_psr.py \
        --pwndata $pwncode/pwndata/pwncat2_data_lande.yaml \
        --pwnphase $pwncode/pwndata/pwncat2_phase_lande.yaml  \
        --modify $pwncode/modify/modify_psr_lande.py \
        -o $pwndata/spectral/test1/analysis_no_plots --no-plots --max-free 5 --no-gtlike

# ----------------------------------------------------------------------------------------------------

echo python $pwncode/loop_pwn.py \
        -c $pwncode/analyze_psr.py \
        --pwndata $pwncode/pwndata/pwncat2_data_lande.yaml \
        --pwnphase $pwncode/pwndata/pwncat2_phase_lande.yaml  \
        --modify $pwncode/modify/modify_psr_lande.py \
        -o $pwndata/spectral/v11/analysis_no_plots --no-plots --max-free 5

echo python $pwncode/loop_pwn.py \
        -c $pwncode/analyze_psr.py \
        --pwndata $pwncode/pwndata/pwncat2_data_lande.yaml \
        --pwnphase $pwncode/pwndata/pwncat2_phase_lande.yaml  \
        --modify $pwncode/modify/modify_psr_lande.py \
        -o $pwndata/spectral/v11/analysis_plots --max-free 5

# ----------------------------------------------------------------------------------------------------


echo python $pwncode/loop_pwn.py \
        --pwndata $pwncode/pwndata/pwncat2_data_lande.yaml \
        -c $pwncode/lande/variability/test_variability.py \
        --analysis-dir $pwndata/spectral/v10/analysis_no_plots \
        -o $pwndata/spectral/v10/variability/v1

# ----------------------------------------------------------------------------------------------------

echo python $pwncode/loop_pwn.py \
        -c $pwncode/analyze_psr.py \
        --pwndata $pwncode/pwndata/pwncat2_data_lande.yaml \
        --pwnphase $pwncode/pwndata/pwncat2_phase_lande.yaml  \
        --modify $pwncode/modify/modify_psr_lande.py \
        -o $pwndata/spectral/v12/analysis_no_plots --no-plots --max-free 5

echo python $pwncode/loop_pwn.py \
        -c $pwncode/analyze_psr.py \
        --pwndata $pwncode/pwndata/pwncat2_data_lande.yaml \
        --pwnphase $pwncode/pwndata/pwncat2_phase_lande.yaml  \
        --modify $pwncode/modify/modify_psr_lande.py \
        -o $pwndata/spectral/v12/analysis_plots --max-free 5

# ----------------------------------------------------------------------------------------------------


echo python $pwncode/loop_pwn.py \
        --pwndata $pwncode/pwndata/pwncat2_data_lande.yaml \
        -c $pwncode/lande/variability/test_variability.py \
        --analysis-dir $pwndata/spectral/v10/analysis_no_plots \
        -o $pwndata/spectral/v10/variability/v2

# ----------------------------------------------------------------------------------------------------


echo python $pwncode/loop_pwn.py \
        --pwndata $pwncode/pwndata/pwncat2_data_lande.yaml \
        -c $pwncode/lande/variability/test_variability.py \
        --analysis-dir $pwndata/spectral/v10/analysis_no_plots \
        -o $pwndata/spectral/v10/variability/v3

# ----------------------------------------------------------------------------------------------------

echo python $pwncode/loop_pwn.py \
        --pwndata $pwncode/pwndata/pwncat2_data_lande.yaml \
        -c $pwncode/lande/variability/test_variability.py \
        --analysis-dir $pwndata/spectral/v10/analysis_no_plots \
        -o $pwndata/spectral/v10/variability/test

# ----------------------------------------------------------------------------------------------------


echo python $pwncode/loop_pwn.py \
        -c $pwncode/analyze_psr.py \
        --pwndata $pwncode/pwndata/pwncat2_data_lande.yaml \
        --pwnphase $pwncode/pwndata/pwncat2_phase_lande.yaml  \
        --modify $pwncode/modify/modify_psr_lande.py \
        -o $pwndata/spectral/v13/analysis_no_plots --no-plots --max-free 5 --no-gtlike --localization-emin=1e2

echo python $pwncode/loop_pwn.py \
        -c $pwncode/analyze_psr.py \
        --pwndata $pwncode/pwndata/pwncat2_data_lande.yaml \
        --pwnphase $pwncode/pwndata/pwncat2_phase_lande.yaml  \
        --modify $pwncode/modify/modify_psr_lande.py \
        -o $pwndata/spectral/v13/analysis_plots --max-free 5 --no-gtlike --localization-emin=1e2

# ----------------------------------------------------------------------------------------------------


echo python $pwncode/loop_pwn.py \
        --pwndata $pwncode/pwndata/pwncat2_data_lande.yaml \
        -c $pwncode/lande/variability/test_variability.py \
        --analysis-dir $pwndata/spectral/v12/analysis_no_plots \
        -o $pwndata/spectral/v12/variability/v1

# ----------------------------------------------------------------------------------------------------


echo python $pwncode/loop_pwn.py \
        --pwndata $pwncode/pwndata/pwncat2_data_lande.yaml \
        -c $pwncode/lande/variability/test_variability.py \
        --analysis-dir $pwndata/spectral/v13/analysis_no_plots \
        -o $pwndata/spectral/v13/variability/v1

# ----------------------------------------------------------------------------------------------------


common_kwargs="--max-free 5 --localization-emin=1e2"
echo python $pwncode/loop_pwn.py \
        -c $pwncode/analyze_psr.py \
        --pwndata $pwncode/pwndata/pwncat2_data_lande.yaml \
        --pwnphase $pwncode/pwndata/pwncat2_phase_lande.yaml  \
        --modify $pwncode/modify/modify_psr_lande.py \
        -o $pwndata/spectral/v14/analysis_no_plots \
        $common_kwargs \
        --no-plots 

echo python $pwncode/loop_pwn.py \
        -c $pwncode/analyze_psr.py \
        --pwndata $pwncode/pwndata/pwncat2_data_lande.yaml \
        --pwnphase $pwncode/pwndata/pwncat2_phase_lande.yaml  \
        --modify $pwncode/modify/modify_psr_lande.py \
        -o $pwndata/spectral/v14/analysis_plots \
        $common_kwargs \
        --no-gtlike --no-cutoff --no-extension-upper-limits --no-upper-limits
 
# ----------------------------------------------------------------------------------------------------


version=v15
common_kwargs="--max-free 5 --localization-emin=1e2"
echo python $pwncode/loop_pwn.py \
        -c \\\$pwncode/analyze_psr.py \
        --pwndata \\\$pwncode/pwndata/pwncat2_data_lande.yaml \
        --pwnphase \\\$pwncode/pwndata/pwncat2_phase_lande.yaml  \
        --modify \\\$pwncode/modify/modify_psr_lande.py \
        -o $pwndata/spectral/$version/analysis_no_plots \
        $common_kwargs \
        --no-plots 

echo python $pwncode/loop_pwn.py \
        -c \\\$pwncode/analyze_psr.py \
        --pwndata \\\$pwncode/pwndata/pwncat2_data_lande.yaml \
        --pwnphase \\\$pwncode/pwndata/pwncat2_phase_lande.yaml  \
        --modify \\\$pwncode/modify/modify_psr_lande.py \
        -o $pwndata/spectral/$version/analysis_plots \
        $common_kwargs \
        --no-gtlike --no-cutoff --no-extension-upper-limits --no-upper-limits

# ----------------------------------------------------------------------------------------------------

# major changes: emax=100 GeV (for now). no savedir. bugfixes
version=v16
common_kwargs="--max-free 5 --localization-emin=1e2 --no-savedir --emax=1e5"
echo python $pwncode/loop_pwn.py \
        -c \\\$pwncode/analyze_psr.py \
        --pwndata \\\$pwncode/pwndata/pwncat2_data_lande.yaml \
        --pwnphase \\\$pwncode/pwndata/pwncat2_phase_lande.yaml  \
        --modify \\\$pwncode/modify/modify_psr_lande.py \
        -o $pwndata/spectral/$version/analysis_no_plots \
        $common_kwargs \
        --no-plots 

echo python $pwncode/loop_pwn.py \
        -c \\\$pwncode/analyze_psr.py \
        --pwndata \\\$pwncode/pwndata/pwncat2_data_lande.yaml \
        --pwnphase \\\$pwncode/pwndata/pwncat2_phase_lande.yaml  \
        --modify \\\$pwncode/modify/modify_psr_lande.py \
        -o $pwndata/spectral/$version/analysis_plots \
        $common_kwargs \
        --no-gtlike --no-cutoff --no-extension-upper-limits --no-upper-limits


# ----------------------------------------------------------------------------------------------------

# major changes: ??? rerun
version=v17
common_kwargs="\$pwncode/loop_pwn.py \
        -c \\\$pwncode/analyze_psr.py \
        --pwndata \\\$pwncode/pwndata/pwncat2_data_lande.yaml \
        --pwnphase \\\$pwncode/pwndata/pwncat2_phase_lande.yaml  \
        --modify \\\$pwncode/modify/modify_psr_lande.py \
        --max-free 5 --localization-emin=1e2 --no-savedir --emax=1e5"

echo python $common_kwargs \
    -o $pwndata/spectral/$version/analysis_no_plots \
    $common_kwargs \
    --no-plots 

echo python $common_kwargs \
        -o $pwndata/spectral/$version/analysis_plots \
        --no-gtlike --no-cutoff --no-extension-upper-limits --no-upper-limits

echo python $common_kwargs \
        -o $pwndata/spectral/$version/analysis_fast \
        --no-gtlike --no-cutoff --no-extension-upper-limits --no-upper-limits --no-plots

echo python $common_kwargs \
        -o $pwndata/spectral/$version/analysis_fast2 \
        --no-gtlike --no-cutoff --no-extension-upper-limits --no-upper-limits --no-plots







# ----------------------------------------------------------------------------------------------------

# major changes: ??? rerun
version=test_v2
common_kwargs="\$pwncode/loop_pwn.py \
        -c \\\$pwncode/analyze_psr.py \
        --pwndata \\\$pwncode/pwndata/pwncat2_data_lande.yaml \
        --pwnphase \\\$pwncode/pwndata/pwncat2_phase_lande.yaml  \
        --modify \\\$pwncode/modify/modify_psr_lande.py \
        --max-free 5 --localization-emin=1e4 --no-savedir --emin=1e4 --emax=1e5 --binsperdec=2"

echo python $common_kwargs \
    -o $pwndata/spectral/$version/analysis_no_plots \
    $common_kwargs \
    --no-plots 

echo python $common_kwargs \
        -o $pwndata/spectral/$version/analysis_plots \
        --no-gtlike --no-cutoff --no-extension-upper-limits --no-upper-limits

echo python $common_kwargs \
        -o $pwndata/spectral/$version/analysis_fast \
        --no-gtlike --no-cutoff --no-extension-upper-limits --no-upper-limits --no-plots




# ----------------------------------------------------------------------------------------------------

# major changes: ??? rerun
version=v18
common_kwargs="\$pwncode/loop_pwn.py \
        -c \\\$pwncode/analyze_psr.py \
        --pwndata \\\$pwncode/pwndata/pwncat2_data_lande.yaml \
        --pwnphase \\\$pwncode/pwndata/pwncat2_phase_lande.yaml  \
        --modify \\\$pwncode/modify/modify_psr_lande.py \
        --max-free 5 --localization-emin=1e2 --no-savedir --emax=1e5"

echo python $common_kwargs \
    -o $pwndata/spectral/$version/analysis_no_plots \
    --no-plots 

echo python $common_kwargs \
        -o $pwndata/spectral/$version/analysis_plots \
        --no-gtlike --no-cutoff --no-extension-upper-limits --no-upper-limits

echo python $common_kwargs \
        -o $pwndata/spectral/$version/analysis_fast \
        --no-gtlike --no-cutoff --no-extension-upper-limits --no-upper-limits --no-plots

echo python $pwncode/loop_pwn.py \
        --pwndata \\\$pwncode/pwndata/pwncat2_data_lande.yaml \
        -c \\\$pwncode/lande/variability/test_variability.py \
        --analysis-dir \\\$pwndata/spectral/v18/analysis_no_plots \
        -o $pwndata/spectral/v18/variability/v1

# ----------------------------------------------------------------------------------------------------


echo python \$pwncode/loop_pwn.py \
        --pwndata \\\$pwncode/pwndata/pwncat2_data_lande.yaml \
        --pwnphase \\\$pwncode/pwndata/pwncat2_phase_lande.yaml  \
        --modify \\\$pwncode/modify/modify_psr_lande.py \
        --max-free 5  --no-savedir --emax=1e5 \
        -o $pwndata/spectral/v19/analysis

# ----------------------------------------------------------------------------------------------------


echo python \$pwncode/loop_pwn.py \
        --pwndata \\\$pwncode/pwndata/pwncat2_data_lande.yaml \
        --pwnphase \\\$pwncode/pwndata/pwncat2_phase_lande.yaml  \
        --modify \\\$pwncode/modify/modify_psr_lande.py \
        --max-free 5  --no-savedir \
        -o $pwndata/spectral/v20/analysis

# ----------------------------------------------------------------------------------------------------



echo python \$pwncode/loop_pwn.py \
        --pwndata \\\$pwncode/pwndata/pwncat2_data_lande.yaml \
        --pwnphase \\\$pwncode/pwndata/pwncat2_phase_lande.yaml  \
        --modify \\\$pwncode/modify/modify_psr_lande.py \
        --max-free 5  --no-savedir \
        -o $pwndata/spectral/v21/analysis

# ----------------------------------------------------------------------------------------------------


echo python \$pwncode/loop_pwn.py \
        --pwndata \\\$pwncode/pwndata/pwncat2_data_lande.yaml \
        --pwnphase \\\$pwncode/pwndata/pwncat2_phase_lande.yaml  \
        --modify \\\$pwncode/modify/modify_psr_lande.py \
        --max-free 5  --no-savedir \
        -o $pwndata/spectral/v22/analysis

# ----------------------------------------------------------------------------------------------------



echo python \$pwncode/loop_pwn.py \
        --pwndata \\\$pwncode/data/pwncat2_data_lande.yaml \
        --pwnphase \\\$pwncode/data/pwncat2_phase_lande.yaml  \
        --modify \\\$pwncode/modify/modify_psr_lande.py \
        --max-free 5  --no-savedir \
        -o $pwndata/spectral/v23/analysis

# ----------------------------------------------------------------------------------------------------


echo python \$pwncode/loop_pwn.py \
        --pwndata \\\$pwncode/data/pwncat2_data_lande.yaml \
        --pwnphase \\\$pwncode/data/pwncat2_phase_lande.yaml  \
        --modify \\\$pwncode/modify/modify_psr_lande.py \
        --max-free 5  --no-savedir \
        -o $pwndata/spectral/v24/analysis

# ----------------------------------------------------------------------------------------------------


echo python \$pwncode/loop_pwn.py \
        --pwndata \\\$pwncode/data/pwncat2_data_lande.yaml \
        --pwnphase \\\$pwncode/data/pwncat2_phase_lande.yaml  \
        --modify \\\$pwncode/modify/modify_psr_lande.py \
        --max-free 5  --no-savedir \
        -o $pwndata/spectral/v25/analysis

# ----------------------------------------------------------------------------------------------------


echo python \$pwncode/loop_pwn.py \
        --pwndata \\\$pwncode/data/pwncat2_data_lande.yaml \
        --pwnphase \\\$pwncode/data/pwncat2_phase_lande.yaml  \
        --modify \\\$pwncode/modify/modify_psr_lande.py \
        --max-free 5  --no-savedir \
        -o $pwndata/spectral/v26/analysis

# ----------------------------------------------------------------------------------------------------


echo python \$pwncode/loop_pwn.py \
        --pwndata \\\$pwncode/data/pwncat2_data_lande.yaml \
        --pwnphase \\\$pwncode/data/pwncat2_phase_lande.yaml  \
        --modify \\\$pwncode/modify/modify_psr_lande.py \
        --max-free 5  --no-savedir \
        -o $pwndata/spectral/v27/analysis

# ----------------------------------------------------------------------------------------------------
