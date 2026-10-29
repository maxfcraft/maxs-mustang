#!/usr/bin/env bash
# Rebuilds mustang.glb from the original Sketchfab download (mustang_gt_2018.zip, glTF format).
# Source: "Mustang_GT 2018" by Demonic Arts, CC BY 4.0
#   https://sketchfab.com/3d-models/mustang-gt-2018-dd4365565b6b4e0ea6c06a1ca4113e3e
# Needs Node. 149.6 MB of glTF + PNG textures -> ~2.2 MB GLB (Draco geometry, 1024px WebP textures).
# Parts are kept separate (no join/palette/flatten) so the page can find the paint, wheels, glass and lights.
set -e
ZIP="${1:-$HOME/Downloads/mustang_gt_2018.zip}"
WORK="$(mktemp -d)"
unzip -q "$ZIP" -d "$WORK/src"
npx -y @gltf-transform/cli@4 optimize "$WORK/src/scene.gltf" mustang.glb \
  --compress draco --texture-compress webp --texture-size 1024 \
  --simplify false --join false --palette false --flatten false --instance false
echo "mustang.glb rebuilt"
