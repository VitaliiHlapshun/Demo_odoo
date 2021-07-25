from odoo import models, fields, api


class Lead(models.Model):
    _inherit = 'crm.lead'

    demo_ids = fields.One2many('demo.demo', 'crm_lead_id')
    demo_count = fields.Integer(string='Quantity', compute='total_demos_calc')

    @api.depends('demo_ids')
    def total_demos_calc(self):
        for demo in self:
            total = 0.0
            for line in demo.demo_ids:
                total += 1
            demo.demo_count = total

    def action_list_view_navigation(self):
        """ This function gets triggered by clicking the button in the button box
        in 'crm_lead' addressing user to the list view of the "demo" module
        """
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id("demo.action_demo")
        return action
