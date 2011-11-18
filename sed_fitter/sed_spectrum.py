
class Spectrum(object):
    """ A spectrum is a base class which represents some
        physical quanity as a function of energy. """

    def loglog(self, emin, emax, e_weight=0, npts=1000, x_units='erg', y_units=None, 
               filename=None, fignum=None, axes=None, **kwargs):
        """ Plots the energy spectrum. 

            emin and emax must have sympy units.
            
            x_units and y_units must be strings suitable
            for plotting on the matplotlib axes. """

        if y_units is None: 
            if e_weight>0:
                y_units = '%s^%s*%s' % ('erg',e_weight,self.units_string())
            else:
                y_units = '%s' % self.units_string()

        if axes is None:
            fig = P.figure(fignum,figsize=(5.5,4.5))
            P.clf()
            fig.subplots_adjust(left=0.18,bottom=0.13,right=0.95,top=0.95)
            axes = fig.add_subplot(111)

        x = np.logspace(np.log10(float(emin/u.erg)), np.log10(float(emax/u.erg)), npts)

        # y is in units of self.units()
        y = x**(e_weight)*self(x, units=False)

        x=u.convert(x,u.erg, u.fromstring(x_units))
        y=u.convert(y,u.erg**(e_weight)*self.units(), u.fromstring(y_units))

        axes.loglog(x,y, **kwargs)
        axes.set_xlabel(x_units)
        axes.set_xlim(x[0],x[-1])

        if e_weight > 0:
            axes.set_ylabel(r'E$^%s$ dN/dE (%s)' % (e_weight,y_units))
        else:
            axes.set_ylabel('dN/dE (%s)' % y_units)
        if filename is not None: P.savefig(filename)
        return axes

    @abstractmethod
    def __call__(self, energy): 
        """ Returns dN/dE. Energy must be in erg. """
        pass

    @classmethod                                                                                                                                                            
    def units(cls):                                                                                                                                                         
        """ Returns the units that __call__ is assumed to be in. """                                                                                                        
        return u.fromstring(cls.units_string())                                                                                                                             

    def __call__(self, energy, units=True):
        """ Returns number of particles per unit energy [1/energy]. """
        if units: energy = float(energy/u.erg)
        spectrum=self.spectrum(energy)
        return spectrum*(self.units() if units else 1)



