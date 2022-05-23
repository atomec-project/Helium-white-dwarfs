from atoMEC import Atom, models, config
import numpy as np
import pickle as pkl

config.numcores=-1

density = 1
temperature = 1

# set up the atom
He_atom = Atom("He", temperature, density=density, units_temp="K")

# set up the model
model = models.ISModel(He_atom, bc="neumann", unbound="quantum")

# run the initial calculation
nmax_guess = 20
lmax_guess = 40
out_test = model.CalcEnergy(
    nmax_guess, lmax_guess, grid_params={"ngrid": 2000}, scf_params={"maxscf": 3}
)

threshold = 1e-3

# get the max values of n and l
occnums = out_test["orbitals"].occnums_w
occnums_n = occnums[0,0,0,:]
occnums_l = occnums[0,0,:,0]
nmax = np.where(occnums_n<threshold)[0][0]
lmax = np.where(occnums_l<threshold)[0][0]

if nmax == 0:
    nmax = nmax_guess
if lmax == 0:
    lmax = lmax_guess
nmax = max(nmax, 3)
lmax = max(lmax, 3)

print("nmax = ",nmax, "lmax = ",lmax)

# run the real calculation
model.bc = "bands"
out = model.CalcEnergy(nmax, lmax, scf_params={"maxscf":50}, band_params={"nkpts":200})

# save the output
with open("He.pkl", "wb") as f:
    pkl.dump(out, f, protocol=pkl.HIGHEST_PROTOCOL)
