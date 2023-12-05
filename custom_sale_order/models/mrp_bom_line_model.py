# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    component_price = fields.Float(string='Precio', related='product_tmpl_id.list_price', store=True, readonly=False)