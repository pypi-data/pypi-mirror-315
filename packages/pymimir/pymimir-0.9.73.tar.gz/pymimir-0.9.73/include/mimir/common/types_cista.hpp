/*
 * Copyright (C) 2023 Dominik Drexler and Simon Stahlberg
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 */

#ifndef MIMIR_COMMON_TYPES_CISTA_HPP_
#define MIMIR_COMMON_TYPES_CISTA_HPP_

#include "cista/containers/dynamic_bitset.h"
#include "cista/containers/vector.h"
#include "mimir/common/types.hpp"
#include "mimir/formalism/declarations.hpp"
#include "mimir/formalism/predicate_tag.hpp"

#include <ostream>

namespace mimir
{
/* Bitset */

using FlatBitset = cista::offset::dynamic_bitset<uint64_t>;

inline std::ostream& operator<<(std::ostream& os, const FlatBitset& set)
{
    os << "[";
    size_t i = 0;
    for (const auto& element : set)
    {
        if (i != 0)
            os << ", ";
        os << element;
        ++i;
    }
    os << "]";
    return os;
}

/* IndexList */

using FlatIndexList = cista::offset::vector<Index>;

inline bool are_disjoint(const FlatBitset& bitset, const FlatIndexList& list)
{
    for (const auto index : list)
    {
        if (bitset.get(index))
        {
            return false;
        }
    }
    return true;
}

inline bool is_superseteq(const FlatBitset& bitset, const FlatIndexList& list)
{
    for (const auto index : list)
    {
        if (!bitset.get(index))
        {
            return false;
        }
    }
    return true;
}

}

#endif
