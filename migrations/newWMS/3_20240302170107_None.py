from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "permissions" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "permission_name" VARCHAR(50) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "permissions"."permission_name" IS 'Permission Name';
COMMENT ON COLUMN "permissions"."created_at" IS 'Created At';
COMMENT ON COLUMN "permissions"."updated_at" IS 'Updated At';
CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(50) NOT NULL,
    "password" VARCHAR(50) NOT NULL,
    "email" VARCHAR(50) NOT NULL,
    "phone" VARCHAR(50) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "users"."username" IS 'Username';
COMMENT ON COLUMN "users"."password" IS 'Password';
COMMENT ON COLUMN "users"."email" IS 'Email';
COMMENT ON COLUMN "users"."phone" IS 'Phone';
COMMENT ON COLUMN "users"."created_at" IS 'Created At';
COMMENT ON COLUMN "users"."updated_at" IS 'Updated At';
CREATE TABLE IF NOT EXISTS "roles" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "role_name" VARCHAR(50) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "users_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "roles"."role_name" IS 'Role Name';
COMMENT ON COLUMN "roles"."created_at" IS 'Created At';
COMMENT ON COLUMN "roles"."updated_at" IS 'Updated At';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "permissions_roles" (
    "permissions_id" INT NOT NULL REFERENCES "permissions" ("id") ON DELETE CASCADE,
    "roles_id" INT NOT NULL REFERENCES "roles" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
