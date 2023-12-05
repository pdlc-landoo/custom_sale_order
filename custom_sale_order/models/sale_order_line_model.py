# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_update_prices(self):
        for line in self.order_line:
            if line.configurable:
                mrp_bom_obj = self.env['mrp.bom'].search([('product_tmpl_id', '=', line.product_template_id.id)])
                if mrp_bom_obj:
                    total_price = 0
                    for component in mrp_bom_obj.bom_line_ids:
                        total_price = total_price + component.component_price
                    line.price_unit = total_price


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    configurable = fields.Boolean(string='Configurable', related='product_template_id.is_configurable', store=True, readonly=False)
    client_order_number = fields.Char(string='S/ Pedido Nº')
    partida = fields.Char(string='Partida')
    warehouse_leaving_order = fields.Char(string='Posición')
    instalacion_id = fields.Char(string='Nºinstalación')
    componentes = fields.Many2one('mrp.bom', 'Componentes')


    @api.onchange('configurable')
    def _onchange_configurable(self):
        if self.configurable:
            mrp_bom_obj = self.env['mrp.bom'].search([('product_tmpl_id', '=', self.product_template_id.id)])
            if mrp_bom_obj:
                total_price = 0
                for component in mrp_bom_obj.bom_line_ids:
                    total_price = total_price + component.component_price
                self.price_unit = total_price
        else:
            if self.qty_invoiced > 0:
                pass
            if not self.product_uom or not self.product_id or not self.order_id.pricelist_id:
                self.price_unit = 0.0
            else:
                price = self.with_company(self.company_id)._get_display_price()
                self.price_unit = self.product_id._get_tax_included_unit_price(
                    self.company_id,
                    self.order_id.currency_id,
                    self.order_id.date_order,
                    'sale',
                    fiscal_position=self.order_id.fiscal_position_id,
                    product_price_unit=price,
                    product_currency=self.currency_id
                )




