actor Person {}

resource Person {
    roles = ["self", "guardian", "group_owner"];
    permissions = ["view", "edit"];
    relations = {
        member_of: Group,
	owner_of: Group
    };

    "group_owner" if "owner" on "member_of";
    "group_owner" if "owner" on "owner_of";

    "view" if "self";
    "view" if "group_owner";
    "view" if "guardian";
}

has_role(actor: Person, "guardian", person: Person) if
    actor in person.guardians;

has_relation(person: Person, "member_of", group: Group) if
    person in group.members or
    person in group.owners;

has_relation(person: Person, "owner_of", group: Group) if
    person in group.owners;

resource Group {
    roles = ["member", "owner"]
    permissions = ["view", "edit"]

    "member" if "owner";

    "view" if "member";
    "edit" if "owner";
}

has_role(actor: Person, "member", group: Group)
    if actor in group.members;

has_role(actor: Person, "owner", group: Group)
    if actor in group.owners;
