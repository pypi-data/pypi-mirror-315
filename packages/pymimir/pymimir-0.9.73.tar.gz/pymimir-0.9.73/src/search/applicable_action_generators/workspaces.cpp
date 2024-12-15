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

#include "mimir/search/applicable_action_generators/workspaces.hpp"

using namespace std::string_literals;

namespace mimir
{

/**
 * LiftedApplicableActionGeneratorWorkspace
 */

AssignmentSetWorkspace& LiftedApplicableActionGeneratorWorkspace::get_or_create_assignment_set_workspace()
{
    if (!assignment_set_workspace.has_value())
    {
        assignment_set_workspace = AssignmentSetWorkspace();
    }

    return assignment_set_workspace.value();
}

SatisficingBindingGeneratorWorkspace& LiftedApplicableActionGeneratorWorkspace::get_or_create_satisficing_binding_generator(Action action)
{
    return satisficing_binding_generator_workspaces[action];
}

/**
 * ApplicableActionGeneratorWorkspace
 */

LiftedApplicableActionGeneratorWorkspace& ApplicableActionGeneratorWorkspace::get_or_create_lifted_workspace(Problem problem)
{
    if (!lifted_workspace.has_value())
    {
        lifted_workspace = LiftedApplicableActionGeneratorWorkspace();
    }

    return lifted_workspace.value();
}

}
