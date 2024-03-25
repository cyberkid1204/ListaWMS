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
    "phone" VARCHAR(50)   DEFAULT '',
    "session_id" VARCHAR(50)   DEFAULT '',
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "users"."username" IS 'Username';
COMMENT ON COLUMN "users"."password" IS 'Password';
COMMENT ON COLUMN "users"."email" IS 'Email';
COMMENT ON COLUMN "users"."phone" IS 'Phone';
COMMENT ON COLUMN "users"."session_id" IS 'Session ID';
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
CREATE TABLE IF NOT EXISTS "inbound_order" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "inbound_order_code" VARCHAR(255) NOT NULL,
    "inbound_order_status" BIGINT NOT NULL  DEFAULT 0,
    "total_weight" DOUBLE PRECISION NOT NULL  DEFAULT 0,
    "total_volume" DOUBLE PRECISION NOT NULL  DEFAULT 0,
    "total_cost" DOUBLE PRECISION NOT NULL  DEFAULT 0,
    "supplier" VARCHAR(255) NOT NULL,
    "creator" VARCHAR(255) NOT NULL,
    "bar_code" VARCHAR(255) NOT NULL,
    "openid" VARCHAR(255) NOT NULL,
    "transportation_fee" JSONB NOT NULL,
    "is_delete" BOOL NOT NULL  DEFAULT False,
    "create_time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "update_time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "inbound_order"."inbound_order_code" IS 'Inbound order code';
COMMENT ON COLUMN "inbound_order"."inbound_order_status" IS 'Inbound order status';
COMMENT ON COLUMN "inbound_order"."total_weight" IS 'Total weight';
COMMENT ON COLUMN "inbound_order"."total_volume" IS 'Total Volume';
COMMENT ON COLUMN "inbound_order"."total_cost" IS 'Total Cost';
COMMENT ON COLUMN "inbound_order"."supplier" IS 'ASN Supplier';
COMMENT ON COLUMN "inbound_order"."creator" IS 'Who Created';
COMMENT ON COLUMN "inbound_order"."bar_code" IS 'Bar Code';
COMMENT ON COLUMN "inbound_order"."openid" IS 'Openid';
COMMENT ON COLUMN "inbound_order"."transportation_fee" IS 'Transportation Fee';
COMMENT ON COLUMN "inbound_order"."is_delete" IS 'Delete Label';
COMMENT ON COLUMN "inbound_order"."create_time" IS 'Create Time';
COMMENT ON COLUMN "inbound_order"."update_time" IS 'Update Time';
CREATE TABLE IF NOT EXISTS "inbound_order_detail" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "supplier" VARCHAR(255) NOT NULL,
    "sku" VARCHAR(255) NOT NULL,
    "sku_name" VARCHAR(255) NOT NULL,
    "sku_bar_code" VARCHAR(255) NOT NULL,
    "sku_weight" DOUBLE PRECISION NOT NULL  DEFAULT 0,
    "sku_volume" DOUBLE PRECISION NOT NULL  DEFAULT 0,
    "sku_cost" DOUBLE PRECISION NOT NULL  DEFAULT 0,
    "sku_quantity" INT NOT NULL  DEFAULT 0,
    "sku_unit" VARCHAR(255) NOT NULL,
    "sku_remark" TEXT NOT NULL,
    "is_delete" BOOL NOT NULL  DEFAULT False,
    "create_time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "update_time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "inbound_order_id_id" INT NOT NULL REFERENCES "inbound_order" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "inbound_order_detail"."supplier" IS 'Supplier';
COMMENT ON COLUMN "inbound_order_detail"."sku" IS 'SKU';
COMMENT ON COLUMN "inbound_order_detail"."sku_name" IS 'SKU Name';
COMMENT ON COLUMN "inbound_order_detail"."sku_bar_code" IS 'SKU Bar Code';
COMMENT ON COLUMN "inbound_order_detail"."sku_weight" IS 'SKU Weight';
COMMENT ON COLUMN "inbound_order_detail"."sku_volume" IS 'SKU Volume';
COMMENT ON COLUMN "inbound_order_detail"."sku_cost" IS 'SKU Cost';
COMMENT ON COLUMN "inbound_order_detail"."sku_quantity" IS 'SKU Quantity';
COMMENT ON COLUMN "inbound_order_detail"."sku_unit" IS 'SKU Unit';
COMMENT ON COLUMN "inbound_order_detail"."sku_remark" IS 'SKU Remark';
COMMENT ON COLUMN "inbound_order_detail"."is_delete" IS 'Delete Label';
COMMENT ON COLUMN "inbound_order_detail"."create_time" IS 'Create Time';
COMMENT ON COLUMN "inbound_order_detail"."update_time" IS 'Update Time';
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
