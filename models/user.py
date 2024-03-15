from tortoise.models import Model
from tortoise import fields


class Users(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, description="Username")
    password = fields.CharField(max_length=50, description="Password")
    email = fields.CharField(max_length=50, description="Email")
    phone = fields.CharField(max_length=50, description="Phone", null=True, default="")
    session_id = fields.CharField(max_length=50, description="Session ID", null=True, default="")
    created_at = fields.DatetimeField(auto_now_add=True, description="Created At")
    updated_at = fields.DatetimeField(auto_now=True, description="Updated At")

    def __str__(self):
        return self.username

    class Meta:
        table = "users"


class Roles(Model):
    id = fields.IntField(pk=True)
    role_name = fields.CharField(max_length=50, description="Role Name")
    created_at = fields.DatetimeField(auto_now_add=True, description="Created At")
    updated_at = fields.DatetimeField(auto_now=True, description="Updated At")
    # 一个角色对应多个用户
    users = fields.ForeignKeyField("ListaWMS.Users", related_name="roles")

    def __str__(self):
        return self.role_name

    class Meta:
        table = "roles"


class Permissions(Model):
    id = fields.IntField(pk=True)
    permission_name = fields.CharField(max_length=50, description="Permission Name")
    created_at = fields.DatetimeField(auto_now_add=True, description="Created At")
    updated_at = fields.DatetimeField(auto_now=True, description="Updated At")
    # 一个权限对应多个角色
    roles = fields.ManyToManyField("ListaWMS.Roles", related_name="permissions")

    def __str__(self):
        return self.permission_name

    class Meta:
        table = "permissions"
