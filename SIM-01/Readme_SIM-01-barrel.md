# SIM-01: CLD Full Simulation with Particle Gun (Barrel Optimized)

## Objective
Run `ddsim` using CLD_o2_v07 geometry and generate 100 electrons with a uniform angular distribution focused on the barrel region (θ = 90°). Output EDM4hep ROOT file and verify detector response.

---

## Simulation Command

```bash
ddsim \
  --steeringFile ./CLDConfig/CLDConfig/cld_steer.py \
  --outputFile electrons_10GeV_barrel.edm4hep.root \
  --numberOfEvents 100 \
  --enableGun \
  --gun.particle e- \
  --gun.energy "10*GeV" \
  --gun.distribution uniform \
  --gun.thetaMin 90 \
  --gun.thetaMax 90 \
  --gun.phiMin 0 \
  --gun.phiMax 360
