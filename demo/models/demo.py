from odoo import models, fields, api


class Demo(models.Model):
    _name = 'demo.demo'
    _description = 'demo.demo'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", required=True, copy=False, readonly=True, index=True,
                       default=lambda self: 'Demo')
    customer = fields.Char(string="Customer", required=True)
    done_date = fields.Date(string="Done Date")
    salesperson = fields.Char(string="Salesperson")
    state = fields.Selection([('cancelled', 'Cancelled'), ('done', 'Done'), ('planned', 'Planned')], default='planned',
                             string="Status", track_visibility='onchange')
    crm_lead_id = fields.Many2one("crm.lead", string="Lead", required=True)

    @api.model
    def default_get(self, fields_list):
        res = super(Demo, self).default_get(fields_list)
        if self.env.context.get('active_model') == "crm.lead":
            lead_id = self.env.context['active_id']
            lead_obj = self.env['crm.lead'].browse(lead_id)
            res['customer'] = lead_obj.partner_id.name
            res['salesperson'] = lead_obj.user_id.name
            res['crm_lead_id'] = lead_obj.id
        return res

    @api.model
    def create(self, vals):
        if vals.get('name', 'Demo') == 'Demo':
            vals['name'] = self.env['ir.sequence'].next_by_code('demo.demo.sequence') or 'Demo'
        result = super(Demo, self).create(vals)
        return result
