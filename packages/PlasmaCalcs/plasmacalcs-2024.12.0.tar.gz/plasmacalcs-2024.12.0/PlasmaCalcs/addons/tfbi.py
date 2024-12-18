"""
File Purpose: Thermal Farley-Buneman Instability add-on.
"""

from .addon_tools import register_addon_loader_if
from ..errors import FormulaMissingError, FluidValueError
from ..quantities import QuantityLoader
from ..tools import (
    ImportFailed,
    UNSET,
)
from ..defaults import DEFAULTS


# if SymSolver or InstabilityTheory imports fail, some methods here will fail,
#  but not all methods --> still useful to load this addon.
try:
    import SymSolver as ss
except ImportError as err:
    ss = ImportFailed("SymSolver", err=err)
try:
    import InstabilityTheory as it
except ImportError as err:
    it = ImportFailed("InstabilityTheory", err=err)

if (DEFAULTS.ADDONS.LOAD_TFBI == True) and any(isinstance(x, ImportFailed) for x in (ss, it)):
    raise ImportError("Failed to import SymSolver or InstabilityTheory. To disable this error, "
                      "Set PlasmaCalcs.defaults.DEFAULTS.LOAD_TFBI to 'attempt' or False.")


@register_addon_loader_if(DEFAULTS.ADDONS.LOAD_TFBI) 
class TfbiLoader(QuantityLoader):
    '''quantities related to the Thermal Farley Buneman Instability.
    
    NOTE: for simple calculations, consider using maindims_means=True!
    '''
    TFBI_VARS = ['mod_B', 'E_un0_perpmag_B', 'kB', 'T_n', 'm_n',  # "global" scalars
                    'm', 'nusn', 'skappa', 'eqperp_ldebye']  # scalars which depend on fluid.

    TFBI_EXTRAS = ['eqperp_lmfp']  # extra vars, relevant to TFBI theory, but not necessary.

    @known_var(deps=TFBI_VARS)
    def get_tfbi_inputs(self, **kw_get_vars):
        '''returns xarray.Dataset of values to input to the tfbi theory.
        "global" scalars (no dependence on component nor fluid)
            'mod_B': |magnetic field|
            'E_un0_perpmag_B': |E_un0 perp to B|. E_un0 = electric field in u_neutral=0 frame.
            'kB': boltzmann constant. kB * T = temperature in energy units.
            'T_n': temperature of neutrals.
            'm_n': mass of neutrals.
        scalars which depend on fluid. Note: checks self.fluid, not self.fluids.
            'm': mass of all non-neutral fluids
            'nusn': collision frequency between fluid and neutrals.
            'skappa': signed magnetization parameter; q |B| / (m nusn)
            'eqperp_ldebye': each fluid's debye length at its "equilibrium" temperature,
                        after considering zeroth order heating due to E_un0_perpmag_B.

        Results depend on self.fluid. May want to call as self('tfbi_inputs', fluid=SET_CHARGED).
        '''
        if any(f.is_neutral() for f in self.iter_fluid()):
            errmsg = ('get_tfbi_inputs expects self.fluid to be charged fluids only,\n'
                      f'but it includes neutrals: {[f for f in self.iter_fluid() if f.is_neutral()]}')
            raise FluidValueError(errmsg)
        # [TODO][EFF] improve efficiency by avoiding redundant calculations,
        #    e.g. B is calculated separately for mod_B, E_un0_perpmag_B, and skappa,
        #    while E_un0 is calculated separately for E_un0_perpmag_B and eqperp_ldebye.
        tfbi_vars = self.TFBI_VARS
        return self(tfbi_vars, **kw_get_vars)

    @known_var(deps=TFBI_EXTRAS)
    def get_tfbi_extras(self, **kw_get_vars):
        '''returns xarray.Dataset of values relevant to TFBI theory but not necessary for inputs.
        Currently this just includes:
            'eqperp_lmfp': each fluid's collisional mean free path at its "equilibrium" temperature,
                        after considering zeroth order heating due to E_un0_perpmag_B.

        Results depend on self.fluid. May want to call as self('tfbi_extras', fluid=SET_CHARGED).
        '''
        if any(f.is_neutral() for f in self.iter_fluid()):
            errmsg = ('get_tfbi_extras expects self.fluid to be charged fluids only,\n'
                      f'but it includes neutrals: {[f for f in self.iter_fluid() if f.is_neutral()]}')
            raise FluidValueError(errmsg)
        tfbi_extras = self.TFBI_EXTRAS
        return self(tfbi_extras, **kw_get_vars)

    @known_var(deps=['tfbi_inputs', 'tfbi_extras'])
    def get_tfbi_all(self, **kw_get_vars):
        '''returns xarray.Dataset of values relevant to TFBI theory.
        This includes tfbi_inputs (required for theory) and tfbi_extras (optional)

        Results depend on self.fluid. May want to call as self('tfbi_all', fluid=SET_CHARGED).
        '''
        return self(['tfbi_inputs', 'tfbi_extras'], **kw_get_vars)
