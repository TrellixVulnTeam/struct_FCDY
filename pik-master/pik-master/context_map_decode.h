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

#ifndef CONTEXT_MAP_DECODE_H_
#define CONTEXT_MAP_DECODE_H_

#include <stdint.h>
#include <vector>

#include "bit_reader.h"

namespace pik {

// Reads the context map from the bit stream. On calling this function,
// context_map->size() must be the number of possible context ids.
// Sets *num_histograms to the number of different histogram ids in
// *context_map.
bool DecodeContextMap(std::vector<uint8_t>* context_map,
                      size_t* num_histograms,
                      BitReader* input);

}  // namespace pik

#endif  // CONTEXT_MAP_DECODE_H_
