from django.db.models.signals import post_save
from django.contrib.auth.models import Group, Permission, User
from django.db.models.signals import post_migrate

from .models import UserProfile

ROLE_GROUPS = {
    'super_admin': {
        'name': 'Super Admin',
        'permissions': 'all',
    },
    'manager': {
        'name': 'Manager',
        'permissions': [
            'add_category', 'change_category', 'delete_category', 'view_category',
            'add_brand', 'change_brand', 'delete_brand', 'view_brand',
            'add_vehicle', 'change_vehicle', 'delete_vehicle', 'view_vehicle',
            'add_product', 'change_product', 'delete_product', 'view_product',
        ],
    },
    'inventory': {
        'name': 'Inventory',
        'permissions': [
            'add_category', 'change_category', 'view_category',
            'add_brand', 'change_brand', 'view_brand',
            'add_vehicle', 'change_vehicle', 'view_vehicle',
            'add_product', 'change_product', 'view_product',
        ],
    },
    'sales': {
        'name': 'Sales',
        'permissions': [
            'view_category',
            'view_brand',
            'view_vehicle',
            'view_product',
        ],
    },
}


def get_tailapp_permissions(codenames):
    queryset = Permission.objects.filter(content_type__app_label='tailapp')

    if codenames == 'all':
        return queryset

    return queryset.filter(codename__in=codenames)


def sync_role_groups():
    for config in ROLE_GROUPS.values():
        group, _ = Group.objects.get_or_create(name=config['name'])
        group.permissions.set(get_tailapp_permissions(config['permissions']))


def apply_profile_role(profile):
    sync_role_groups()

    managed_group_names = [config['name'] for config in ROLE_GROUPS.values()]
    profile.user.groups.remove(
        *Group.objects.filter(name__in=managed_group_names)
    )

    role_config = ROLE_GROUPS.get(profile.role)
    if role_config:
        group = Group.objects.get(name=role_config['name'])
        profile.user.groups.add(group)


def create_profile(sender,instance,created,**kwargs):

    if created:

        UserProfile.objects.create(
            user=instance,
            role='super_admin' if instance.is_superuser else 'inventory'
        )


def update_role_group(sender, instance, **kwargs):
    apply_profile_role(instance)


def create_role_groups(sender, **kwargs):
    sync_role_groups()
    for profile in UserProfile.objects.select_related('user'):
        if profile.user.is_superuser and profile.role != 'super_admin':
            profile.role = 'super_admin'
            profile.save(update_fields=['role'])
        else:
            apply_profile_role(profile)


post_save.connect(
    create_profile,
    sender=User
)

post_save.connect(
    update_role_group,
    sender=UserProfile
)

post_migrate.connect(create_role_groups)
