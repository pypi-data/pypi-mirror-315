import h5py

fh = h5py.File("HSC_template_integrals_yfix.h5", "r+")

z = fh["z"]
del fh["z"]
fh["z"] = z[::100]

for integral, integrals in fh["integrals"].items():
    print(integral)
    for name, template in integrals.items():
        print("  ", name, template.shape)
        del integrals[name]
        integrals[name] = template[::100, :]
