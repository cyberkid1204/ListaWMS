# !/usr/bin/env python
# -*-   coding:utf-8   -*-
# Author     ：NanZhou
# version    ：python 3.11
# =============================================
from tortoise.models import Model
from tortoise import fields


class InboundOrder(Model):
    id = fields.IntField(pk=True)
    inbound_order_code = fields.CharField(
        max_length=255, description="Inbound order code"
    )
    inbound_order_status = fields.BigIntField(
        default=0, description="Inbound order status"
    )
    total_weight = fields.FloatField(default=0, description="Total weight")
    total_volume = fields.FloatField(default=0, description="Total Volume")
    total_cost = fields.FloatField(default=0, description="Total Cost")
    supplier = fields.CharField(max_length=255, description="ASN Supplier")
    creator = fields.CharField(max_length=255, description="Who Created")
    bar_code = fields.CharField(max_length=255, description="Bar Code")
    openid = fields.CharField(max_length=255, description="Openid")
    transportation_fee = fields.JSONField(
        default=dict, description="Transportation Fee"
    )
    is_delete = fields.BooleanField(default=False, description="Delete Label")
    create_time = fields.DatetimeField(auto_now_add=True, description="Create Time")
    update_time = fields.DatetimeField(auto_now=True, description="Update Time")

    class Meta:
        table = "inbound_order"
        schema = "order"
        ordering = ["-id"]


class InboundOrderDetail(Model):
    id = fields.IntField(pk=True)
    inbound_order_id = fields.ForeignKeyField(
        "ListaWMS.InboundOrder", related_name="inbound_order_detail"
    )
    supplier = fields.CharField(max_length=255, description="Supplier")
    sku = fields.CharField(max_length=255, description="SKU")
    sku_name = fields.CharField(max_length=255, description="SKU Name")
    sku_bar_code = fields.CharField(max_length=255, description="SKU Bar Code")
    sku_weight = fields.FloatField(default=0, description="SKU Weight")
    sku_volume = fields.FloatField(default=0, description="SKU Volume")
    sku_cost = fields.FloatField(default=0, description="SKU Cost")
    sku_quantity = fields.IntField(default=0, description="SKU Quantity")
    sku_unit = fields.CharField(max_length=255, description="SKU Unit")
    sku_remark = fields.TextField(description="SKU Remark")
    is_delete = fields.BooleanField(default=False, description="Delete Label")
    create_time = fields.DatetimeField(auto_now_add=True, description="Create Time")
    update_time = fields.DatetimeField(auto_now=True, description="Update Time")

    class Meta:
        table = "inbound_order_detail"
        schema = "order"
        ordering = ["-id"]
