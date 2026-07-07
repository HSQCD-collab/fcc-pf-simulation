# SIM-01 Electron Gun Baseline

This folder contains the Week 1 SIM-01 validation work for CLD full simulation using `ddsim`.

## Objective

The goal is to run a basic CLD full simulation using a 10 GeV electron particle gun and verify that the EDM4hep output file contains the expected simulation collections.

The main required checks are:

* ROOT output file exists.
* `MCParticles` is present and non-empty.
* `ECalBarrelCollection` is present and checked.
* `HCalBarrelCollection` is present and checked.
* A short note documents the command flags and validation result.

## Folder Contents

```text
electron_gun_baseline/
  README.md
  commands/
    README_commands.md
    run_electron_10GeV_uniform.sh
    run_electron_10GeV_barrel.sh
  scripts/
    inspect_sim_file.py
  logs/
    inspect_uniform.txt
    inspect_barrel.txt
```

## Generated Samples

Two samples were produced:

| Sample               | Output file                                       | Purpose                                     |
| -------------------- | ------------------------------------------------- | ------------------------------------------- |
| Uniform electron gun | `electrons_10GeV_uniform_CLD_o2_v07.edm4hep.root` | Main SIM-01 baseline sample                 |
| Barrel electron gun  | `electrons_10GeV_barrel_CLD_o2_v07.edm4hep.root`  | Control sample focused on the barrel region |

The ROOT files are not committed to GitHub. They should be stored externally, for example on CERNBox or EOS.

## Inspection Script

The validation script is:

```bash
scripts/inspect_sim_file.py
```

Run it with:

```bash
python scripts/inspect_sim_file.py electrons_10GeV_uniform_CLD_o2_v07.edm4hep.root \
  --output logs/inspect_uniform.txt
```

and:

```bash
python scripts/inspect_sim_file.py electrons_10GeV_barrel_CLD_o2_v07.edm4hep.root \
  --output logs/inspect_barrel.txt
```

The script prints and saves:

* top-level ROOT objects,
* trees and branches,
* event collection occupancy over all 100 events,
* a short Week 1 summary for important collections.

## Validation Results

### Uniform sample

The uniform sample contains 100 events. The important Week 1 collections were found and verified:

| Collection             | Non-empty events | Total objects |
| ---------------------- | ---------------: | ------------: |
| `MCParticles`          |          100/100 |           512 |
| `ECalBarrelCollection` |           89/100 |         18136 |
| `ECalEndcapCollection` |           72/100 |         17298 |
| `HCalBarrelCollection` |           47/100 |           196 |
| `HCalEndcapCollection` |           41/100 |           534 |

Because the gun direction is uniform, particles populate both barrel and endcap regions.

### Barrel sample

The barrel sample also contains 100 events. The important Week 1 collections were found and verified:

| Collection             | Non-empty events | Total objects |
| ---------------------- | ---------------: | ------------: |
| `MCParticles`          |          100/100 |           406 |
| `ECalBarrelCollection` |          100/100 |         38982 |
| `ECalEndcapCollection` |           53/100 |           191 |
| `HCalBarrelCollection` |           84/100 |           393 |
| `HCalEndcapCollection` |            6/100 |            17 |

The barrel sample has much stronger barrel activity, as expected from the fixed `theta = 90°` configuration.

