// Copyright 2019 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include "REDACTEDsubmissions/training/v0_7/models/prod/minigo/cc/model/types.h"

namespace minigo {

std::ostream& operator<<(std::ostream& os, const TensorShape& shape) {
  os << "[";
  if (!shape.empty()) {
    os << shape[0];
    for (int i = 1; i < shape.size(); ++i) {
      os << ", " << shape[i];
    }
  }
  os << "]";
  return os;
}

}  // namespace minigo
