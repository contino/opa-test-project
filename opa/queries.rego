package contino.terraform.queries

# the resource changes (names)
resource_changes[resources] {
  resource_changes_actions[resources] = _
}

# the actions for the given resource that are allowed
allowed_resource_changes[resource_name] = allowed_changes {
  allowed_changes = data.constraints.approved_changes[resource_name]
}

used_provider_version[provider_name] = version_constraint {
  some raw_name                                    
  data.plan.configuration.provider_config[raw_name] = _
  version_constraint := data.plan.configuration.provider_config[raw_name].version_constraint
  names := regex.split(":", raw_name)
  provider_name := names[count(names) - 1]
}

# the actions for the given resource that are planned
resource_changes_actions[resource_name] = actions {
  data.plan.resource_changes[_].type = type
  data.plan.resource_changes[_].name = name
  data.plan.resource_changes[_].module_address = module_address
  resource_name = concat(".", [type, name])
  full_address =  concat(".", [module_address, resource_name])
  resources := [x | x = data.plan.resource_changes[_]; x.address == full_address]
  actions := resources[_].change.actions
}

