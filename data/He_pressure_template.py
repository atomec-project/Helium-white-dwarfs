from atoMEC import Atom, models, config, unitconv
from atoMEC.postprocess import pressure
import numpy as np
import pickle as pkl
import sys

config.numcores = -1

density = 1
temperature = 1

# set up the atom
He_atom = Atom("He", temperature, density=density, units_temp="K")

# set up the model
model =models.ISModel(He_atom, bc="bands", unbound="quantum")

# load in the pkl file
try:
    with open("He.pkl", "rb") as f:
        out = pkl.load(f)
except FileNotFoundError:
    sys.exit()

# extract nmax and lmax parameters
orbs = out["orbitals"]
pot = out["potential"]
nkpts, npsin, lmax, nmax, ngrid = np.shape(orbs.eigfuncs)

# finite difference pressure
P_fd = model.CalcPressure(
    He_atom,
    out,
    nmax=nmax,
    lmax=lmax,
    scf_params={"maxscf": 50},
    band_params={"nkpts": nkpts},
    grid_params={"ngrid": ngrid},
)

# stress-tensor pressure
P_st = pressure.stress_tensor(orbs, pot)[-1]

# ion pressure
P_ion = pressure.ions_ideal(He_atom)

# print outputs
print("Pressure FD = ", P_fd * unitconv.ha_to_gpa)
print("Pressure ST = ", P_st * unitconv.ha_to_gpa)
print("Pressure ions = ", P_ion * unitconv.ha_to_gpa)

P_dict = {"P_FD": P_fd, "P_st": P_st, "P_ion": P_ion}

# save the output
with open("Pressure.pkl", "wb") as f:
    pkl.dump(P_dict, f, protocol=pkl.HIGHEST_PROTOCOL)


