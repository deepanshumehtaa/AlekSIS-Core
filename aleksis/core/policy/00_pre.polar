# Evaluate shorthand rules
allow(actor, action, resource) if has_permission(actor, action, resource);

# Define self role for all objects
has_role(actor: Actor, "self", resource: Resource) if
    actor == resource;
