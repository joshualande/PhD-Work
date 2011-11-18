from sed
if __name__ == '__main__':

    # all the code below is for testing out the main code.

    def test_spectra():
        p = PowerLaw(total_energy = 2e48*u.erg, index=2.6,
                     emin=1e-6*u.eV,emax=1e14*u.eV)
        #ax=p.loglog(u.keV,u.MeV, e_weight=2, filename='sed.png')
        print 'total electron energy,',u.repr(p.integral(e_weight=1,units=True),'erg')
    #test_spectra()

    def test_thermal():
        cmb=CMB()
        emin=1e-3*cmb.kT*u.erg
        emax=1e2*cmb.kT*u.erg
        cmb.loglog(emin=emin, emax=emax, 
                   e_weight=2, 
                   x_units='2.725*kelvin*boltzmann',
                   filename='cmb.png')

    #test_thermal()

    def stefan_hess_j1813():
        electron_spectrum = BrokenPowerLawCutoff(
                total_energy = 2e48*u.erg,
                index1 = 2.0,
                index2 = 3.0,
                e_break = 1e7*u.eV,
                e_cutoff = 1.e14*u.eV,
                emin=1e-6*u.eV,
                emax=1e17*u.eV)

        print 'total electron energy %s' % u.repr(electron_spectrum.integral(e_weight=1,units=True),'erg')
        emin=1e-7*u.eV
        emax=1e15*u.eV

        electron_spectrum.loglog(emin=emin, emax=emax, 
                   e_weight=2, x_units='eV', y_units='eV', 
                   filename='ElectronSpectrum.png')

        synch = Synchrotron(electron_spectrum=electron_spectrum,
                            magnetic_field=3e-6*u.gauss)

        cmb=CMB()

        ic = InverseCompton(electron_spectrum=electron_spectrum,
                            photon_spectrum = cmb)


        plot_sed(synch,distance=4.2*u.kpc)
        #plot_sed(ic,distance=4.2*u.kpc)


    stefan_hess_j1813()

    def test_thermal_spectrum():
        cmb=CMB()
        print 'kt=',cmb.kT
        print 'dnde=',cmb(cmb.kT)
        total_energy_density = cmb.integrate(e_weight=1)
        print 'total',total_energy_density
        print 'computed = ', u.repr(total_energy_density,'eV/m^3')
        print 'from stefan = 2.60e5 eV/m^3'

    #test_thermal_spectrum()

    def yasunobu_w51c():
        pass
    #yasunobu_w51c()

