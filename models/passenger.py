# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date


class SaleOrderPassenger(models.Model):
    _name = 'sale.order.passenger'
    _description = 'Passenger Details'

    sale_order_id = fields.Many2one(
        'sale.order',
        string='Sale Order',
        ondelete='cascade',
        required=True
    )

    name = fields.Char(string='Passenger Name', required=True)
    passport_no = fields.Char(string='رقم جواز السفر')
    gender = fields.Selection(
        [('m', 'ذكر'), ('f', 'أنثى')],
        string="النوع"
    )
    birth_date = fields.Date(string='تاريخ الميلاد')
    age = fields.Integer(
        string='العمر',
        compute='_compute_age',
        store=True
    )
    age_category = fields.Selection(
        [('infant', 'Infant'), ('child', 'Child'), ('adult', 'Adult')],
        string='فئة العمر',
        compute='_compute_age_category',
        store=True
    )
    booking_ref = fields.Char(string='مرجع التذكرة')
    ticket_no1 = fields.Char(string='Ticket No.1 - First Way')
    ticket_no2 = fields.Char(string='Ticket No.2 - Return')
    room_type = fields.Selection([
        ('double', 'Double'),
        ('triple', 'Triple'),
        ('quad', 'Quadruple'),
        ('quint', 'Quintuple')
    ], string='Room Type')
    
    room_nbr =  fields.Char(string='Room Number')


    @api.depends('birth_date')
    def _compute_age(self):
        """Compute age from birth_date."""
        today = date.today()
        for passenger in self:
            if passenger.birth_date:
                # Calculate age considering whether birthday has passed this year
                birth_date = passenger.birth_date
                passenger.age = (
                    today.year - birth_date.year
                    - ((today.month, today.day) < (birth_date.month, birth_date.day))
                )
            else:
                passenger.age = 0

    @api.depends('age')
    def _compute_age_category(self):
        """Compute age category: Infant (<2), Child (<12), Adult (>=12)"""
        for passenger in self:
            if passenger.age < 2:
                passenger.age_category = 'infant'
            elif passenger.age < 12:
                passenger.age_category = 'child'
            else:
                passenger.age_category = 'adult'

    @api.constrains('birth_date')
    def _check_birth_date(self):
        """Ensure birth date is not in the future."""
        today = date.today()
        for record in self:
            if record.birth_date and record.birth_date > today:
                raise ValidationError(_("تاريخ الميلاد لا يمكن أن يكون في المستقبل."))