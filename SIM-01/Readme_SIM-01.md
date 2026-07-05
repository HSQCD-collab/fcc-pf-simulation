# SIM-01

## Command

```bash
ddsim \
  --steeringFile cld_steer.py \
  --outputFile electrons_10GeV.edm4hep.root \
  --numberOfEvents 100 \
  --enableGun \
  --gun.particle e- \
  --gun.energy "10*GeV"
```

## Flags

| Flag | Purpose |
|------|---------|
| --steeringFile | Steering configuration |
| --outputFile | Output EDM4hep ROOT file |
| --numberOfEvents | Generate 100 events |
| --enableGun | Enable particle gun |
| --gun.particle | Electron beam |
| --gun.energy | Set beam energy to 10 GeV |

## Verification

Verified the following collections exist:

- MCParticles
- ECalBarrelCollection
- HCalBarrelCollection

All collections are non-empty.
