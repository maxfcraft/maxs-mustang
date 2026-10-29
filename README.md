# Max's Mustang

An interactive 3D garage for my 2018 Mustang. Spin it, swap the wheels, black out the rims, flip on Halloween mode.

**Live:** https://maxfcraft.github.io/maxs-mustang/

Built with three.js: a detailing bay with a honeycomb LED ceiling, a mirror-finish floor, clearcoat paint, bloom, and soft shadows. Works on phones.

## Credits
- 3D model: ["Mustang_GT 2018"](https://sketchfab.com/3d-models/mustang-gt-2018-dd4365565b6b4e0ea6c06a1ca4113e3e) by Demonic Arts, licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Repainted, recompressed, and fitted with optional custom wheels.
- Everything else (studio, lighting, wheels, Halloween props, UI) built by Max with Claude.

## Rebuild
- `_build/build_model.sh` turns the original Sketchfab download into `mustang.glb`.
- `_build/patch_real_model.py` is the one-time patch that swapped the hand-built body for the real model.
