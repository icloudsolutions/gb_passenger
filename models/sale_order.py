# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    passenger_ids = fields.One2many(
        'sale.order.passenger',
        'sale_order_id',
        string='الركاب',
        copy=True
    )
    passenger_count = fields.Integer(
        string='عدد الركاب',
        compute='_compute_passenger_count',
        store=True
    )

    event_id = fields.Many2one('event.event', string='Tour')

    @api.depends('passenger_ids')
    def _compute_passenger_count(self):
        """Compute the number of passengers linked to the sale order."""
        for order in self:
            order.passenger_count = len(order.passenger_ids)


