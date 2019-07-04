package contino.rules

import data.contino.terraform.queries as tq

# Check if the provider is in the approved provider list, and has the correct version
is_approved_provider(name, version) {
  data.constraints.approved_providers[name].version == version
}

# Have all defined providers has their version constraints defined?
default used_providers_have_version_constraint = false
used_providers_have_version_constraint {
  used_providers = data.plan.configuration.provider_config
  providers_with_versions := tq.used_provider_version
  count(used_providers) == count(providers_with_versions)
}

# Are all providers on the approved provider list?
default using_allowed_providers = false
using_allowed_providers {
  providers_with_versions := tq.used_provider_version
  count(providers_with_versions) == count([version | version = providers_with_versions[name]; is_approved_provider(name, version)])
}

# a predicate for actions that are not within the allowed
resource_actions_disallowed(resource_name) {
  actions := tq.resource_changes_actions[resource_name]
  allowed_actions := tq.allowed_resource_changes[resource_name]
  count(cast_set(actions) - cast_set(allowed_actions)) > 0
}

# Are all resource changes approved?
default all_resource_changes_approved = false
all_resource_changes_approved {
  count([r | r = tq.resource_changes[_]; tq.allowed_resource_changes[r]]) == count(tq.resource_changes)
  count([x | x = tq.resource_changes[_]; resource_actions_disallowed(x)]) == 0
}

default allow = false
allow {
  all_resource_changes_approved
  used_providers_have_version_constraint
  using_allowed_providers
}