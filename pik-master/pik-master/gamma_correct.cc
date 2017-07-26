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

#include "gamma_correct.h"

#include <stddef.h>
#include <array>
#include <cmath>
#include <utility>

#include "compiler_specific.h"
#include "profiler.h"

namespace pik {

const float* NewSrgb8ToLinearTable() {
  float* table = new float[256];
  for (int i = 0; i < 256; ++i) {
    table[i] = Srgb8ToLinearDirect(i);
  }
  return table;
}

const float* Srgb8ToLinearTable() {
  static const float* const kSrgb8ToLinearTable = NewSrgb8ToLinearTable();
  return kSrgb8ToLinearTable;
}

const uint8_t* NewLinearToSrgb8Table() {
  uint8_t* table = new uint8_t[4096];
  for (int i = 0; i < 4096; ++i) {
    table[i] = std::round(LinearToSrgb8Direct(i / 16.0));
  }
  return table;
}

const uint8_t* LinearToSrgb8Table() {
  static const uint8_t* const kLinearToSrgb8Table = NewLinearToSrgb8Table();
  return kLinearToSrgb8Table;
}

ImageF LinearFromSrgb(const ImageB& srgb) {
  PROFILER_FUNC;
  const float* lut = Srgb8ToLinearTable();
  const size_t xsize = srgb.xsize();
  const size_t ysize = srgb.ysize();
  ImageF linear(xsize, ysize);
  for (size_t y = 0; y < ysize; ++y) {
    const uint8_t* const PIK_RESTRICT row = srgb.Row(y);
    float* const PIK_RESTRICT row_linear = linear.Row(y);
    for (size_t x = 0; x < xsize; ++x) {
      row_linear[x] = lut[row[x]];
    }
  }
  return linear;
}

Image3F LinearFromSrgb(const Image3B& srgb) {
  return Image3F(LinearFromSrgb(srgb.plane(0)), LinearFromSrgb(srgb.plane(1)),
                 LinearFromSrgb(srgb.plane(2)));
}

ImageB SrgbFromLinear(const ImageF& linear) {
  PROFILER_FUNC;
  const size_t xsize = linear.xsize();
  const size_t ysize = linear.ysize();
  ImageB srgb(xsize, ysize);
  for (size_t y = 0; y < ysize; ++y) {
    const float* const PIK_RESTRICT row_linear = linear.Row(y);
    uint8_t* const PIK_RESTRICT row = srgb.Row(y);
    for (size_t x = 0; x < xsize; ++x) {
      row[x] = static_cast<uint8_t>(
          std::round(LinearToSrgb8Direct(row_linear[x])));
    }
  }
  return srgb;
}

Image3B SrgbFromLinear(const Image3F& linear) {
  return Image3B(SrgbFromLinear(linear.plane(0)),
                 SrgbFromLinear(linear.plane(1)),
                 SrgbFromLinear(linear.plane(2)));
}

ImageF SrgbFFromLinear(const ImageF& linear) {
  PROFILER_FUNC;
  const size_t xsize = linear.xsize();
  const size_t ysize = linear.ysize();
  ImageF srgb(xsize, ysize);
  for (size_t y = 0; y < ysize; ++y) {
    const float* const PIK_RESTRICT row_linear = linear.Row(y);
    float* const PIK_RESTRICT row = srgb.Row(y);
    for (size_t x = 0; x < xsize; ++x) {
      row[x] = LinearToSrgb8Direct(row_linear[x]);
    }
  }
  return srgb;
}

Image3F SrgbFFromLinear(const Image3F& linear) {
  return Image3F(SrgbFFromLinear(linear.plane(0)),
                 SrgbFFromLinear(linear.plane(1)),
                 SrgbFFromLinear(linear.plane(2)));
}

}  // namespace pik
