from django.utils.encoding import force_text
from django_auth_ldap.config import LDAPGroupType


class PosixGroupType(LDAPGroupType):
    """
    An LDAPGroupType subclass that handles groups of class posixGroup.
    """
    def user_groups(self, ldap_user, group_search):
        """
        Searches for any group that is either the user's primary or contains the
        user as a member.
        """
        groups = []

        try:
            user_uid = ldap_user.attrs['uid'][0]

            # if 'gidNumber' in ldap_user.attrs:
            #     user_gid = ldap_user.attrs['gidNumber'][0]
            #     filterstr = '(|(gidNumber={})(memberUid={}))'.format(
            #         self.ldap.filter.escape_filter_chars(user_gid),
            #         self.ldap.filter.escape_filter_chars(user_uid)
            #     )
            # else:
            filterstr = '(memberUid={})'.format(
                self.ldap.filter.escape_filter_chars(user_uid),
            )

            search = group_search.search_with_additional_term_string(filterstr)
            groups = search.execute(ldap_user.connection)
        except (KeyError, IndexError):
            pass

        return groups

    def is_member(self, ldap_user, group_dn):
        """
        Returns True if the group is the user's primary group or if the user is
        listed in the group's memberUid attribute.
        """
        try:
            user_uid = ldap_user.attrs['uid'][0]

            try:
                is_member = ldap_user.connection.compare_s(
                    force_text(group_dn),
                    'memberUid',
                    user_uid.encode('utf-8'),
                )
            except (ldap.UNDEFINED_TYPE, ldap.NO_SUCH_ATTRIBUTE):
                is_member = False

            if not is_member:
                try:
                    user_gid = ldap_user.attrs['gidNumber'][0]
                    is_member = ldap_user.connection.compare_s(
                        force_text(group_dn),
                        'gidNumber',
                        user_gid.encode('utf-8'),
                    )
                except (ldap.UNDEFINED_TYPE, ldap.NO_SUCH_ATTRIBUTE):
                    is_member = False
        except (KeyError, IndexError):
            is_member = False

        return is_member

