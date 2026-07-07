ddsim \
  --steeringFile ./CLDConfig/CLDConfig/cld_steer.py \
  --compactFile $K4GEO/FCCee/CLD/compact/CLD_o2_v07/CLD_o2_v07.xml \
  --enableGun \
  --gun.particle e- \
  --gun.energy "10*GeV" \
  --gun.distribution uniform \
  --numberOfEvents 100 \
  --outputFile electrons_10GeV_uniform_CLD_o2_v07.edm4hep.root