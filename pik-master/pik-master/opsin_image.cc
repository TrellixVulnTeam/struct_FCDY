// Copyright 2017 Google Inc. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include "opsin_image.h"

#include <array>
#include <cmath>

#include "approx_cube_root.h"

namespace pik {

namespace {

float Srgb8ToOpsinDirect(float val) {
  if (val <= 0.0) {
    return 0.0;
  }
  if (val >= 255.0) {
    return 255.0;
  }
  if (val <= kGammaInitialCutoff) {
    return val / kGammaInitialSlope;
  }
  return 255.0 * std::pow(((val / 255.0) + kGammaOffset) /
                          (1.0 + kGammaOffset), kGammaPower);
}

const float* NewSrgb8ToOpsinTable() {
  float* table = new float[256];
  for (int i = 0; i < 256; ++i) {
    table[i] = Srgb8ToOpsinDirect(i);
  }
  return table;
}

PIK_INLINE float SimpleGamma(float v) {
  return ApproxCubeRoot(v);
}

void LinearXybTransform(float r, float g, float b, float* PIK_RESTRICT valx,
                        float* PIK_RESTRICT valy, float* PIK_RESTRICT valz) {
  *valx = (kScaleR * r - kScaleG * g) * 0.5f;
  *valy = (kScaleR * r + kScaleG * g) * 0.5f;
  *valz = b;
}

}  // namespace

const float* Srgb8ToOpsinTable() {
  static const float* const kSrgb8ToOpsinTable = NewSrgb8ToOpsinTable();
  return kSrgb8ToOpsinTable;
}

void RgbToXyb(uint8_t r, uint8_t g, uint8_t b, float* PIK_RESTRICT valx,
              float* PIK_RESTRICT valy, float* PIK_RESTRICT valz) {
  // TODO(janwas): replace with polynomial to enable vectorization.
  const float* lut = Srgb8ToOpsinTable();
  const float rgb[3] = {lut[r], lut[g], lut[b]};
  float mixed[3];
  OpsinAbsorbance(rgb, mixed);
  mixed[0] = SimpleGamma(mixed[0]);
  mixed[1] = SimpleGamma(mixed[1]);
  mixed[2] = SimpleGamma(mixed[2]);
  LinearXybTransform(mixed[0], mixed[1], mixed[2], valx, valy, valz);
}

Image3F OpsinDynamicsImage(const Image3B& srgb) {
  // This is different from butteraugli::OpsinDynamicsImage() in the sense that
  // it does not contain a sensitivity multiplier based on the blurred image.
  const size_t xsize = srgb.xsize();
  const size_t ysize = srgb.ysize();
  Image3F opsin(xsize, ysize);
  for (size_t iy = 0; iy < ysize; iy++) {
    const auto row_in = srgb.ConstRow(iy);
    auto row_out = opsin.Row(iy);
    for (size_t ix = 0; ix < xsize; ix++) {
      RgbToXyb(row_in[0][ix], row_in[1][ix], row_in[2][ix], &row_out[0][ix],
               &row_out[1][ix], &row_out[2][ix]);
    }
  }
  return opsin;
}

}  // namespace pik
