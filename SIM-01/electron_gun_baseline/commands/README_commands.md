# SIM-01 Commands

This folder contains the `ddsim` commands used for the Week 1 SIM-01 electron gun validation.

## SIM-01 Goal

Run `ddsim` with the CLD_o2_v07 detector geometry and generate 100 single electrons at 10 GeV. The output should be an EDM4hep ROOT file. The required collections to verify are:

* `MCParticles`
* `ECalBarrelCollection`
* `HCalBarrelCollection`

## 1. Uniform Electron Gun Sample

```bash
ddsim \
  --steeringFile ./CLDConfig/CLDConfig/cld_steer.py \
  --compactFile $K4GEO/FCCee/CLD/compact/CLD_o2_v07/CLD_o2_v07.xml \
  --enableGun \
  --gun.particle e- \
  --gun.energy "10*GeV" \
  --gun.distribution uniform \
  --numberOfEvents 100 \
  --outputFile electrons_10GeV_uniform_CLD_o2_v07.edm4hep.root
```

This is the main SIM-01 baseline sample. The particle direction is generated with a uniform angular distribution, so events can populate both barrel and endcap detector regions.

## 2. Barrel-Controlled Electron Gun Sample

```bash
ddsim \
  --steeringFile ./CLDConfig/CLDConfig/cld_steer.py \
  --compactFile $K4GEO/FCCee/CLD/compact/CLD_o2_v07/CLD_o2_v07.xml \
  --enableGun \
  --gun.particle e- \
  --gun.energy "10*GeV" \
  --gun.distribution uniform \
  --gun.thetaMin 90 \
  --gun.thetaMax 90 \
  --gun.phiMin 0 \
  --gun.phiMax 360 \
  --numberOfEvents 100 \
  --outputFile electrons_10GeV_barrel_CLD_o2_v07.edm4hep.root
```

This is a control sample. The polar angle is fixed at `theta = 90°`, so the primary electrons are directed through the barrel region.

## Flag Summary

| Flag                                     | Meaning                                                                 |
| ---------------------------------------- | ----------------------------------------------------------------------- |
| `--steeringFile`                         | Loads the CLD steering configuration.                                   |
| `--compactFile`                          | Selects the CLD_o2_v07 detector geometry.                               |
| `--enableGun`                            | Enables the internal DDSim particle gun.                                |
| `--gun.particle e-`                      | Generates electrons.                                                    |
| `--gun.energy "10*GeV"`                  | Sets the electron energy to 10 GeV.                                     |
| `--gun.distribution uniform`             | Randomizes the particle direction using a uniform angular distribution. |
| `--gun.thetaMin 90`, `--gun.thetaMax 90` | Restricts the barrel-control sample to transverse particles.            |
| `--gun.phiMin 0`, `--gun.phiMax 360`     | Allows full azimuthal coverage around the detector.                     |
| `--numberOfEvents 100`                   | Simulates 100 events.                                                   |
| `--outputFile`                           | Sets the EDM4hep ROOT output file name.                                 |

## Difference Between the Two Commands

The uniform sample is the main SIM-01 sample. It tests the detector response over a broad angular region.

The barrel sample is a controlled comparison sample. It forces the particles into the barrel and is useful for checking barrel calorimeter and tracker collections.
