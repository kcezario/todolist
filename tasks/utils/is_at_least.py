from tasks.constants import GROUP_HIERARCHY 

def is_at_least(user, group_name):
    """
    Check if a user belongs to the specified group or a higher one.

    :param user: Django User instance
    :param group_name: Minimum required group
    :return: True if the user belongs to the required group or higher, False otherwise
    """
    if not user.is_authenticated:
        return False

    required_level = GROUP_HIERARCHY.get(group_name)

    if required_level is None:
        raise ValueError(f"Group '{group_name}' not found in hierarchy.")

    user_groups = user.groups.all().values_list("name", flat=True)

    for group in user_groups:
        if GROUP_HIERARCHY.get(group, 0) >= required_level:
            return True

    return False
