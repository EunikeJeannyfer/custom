# from odoo import models, fields, api, _
# #from odoo yg digunakan adalah u working directory
# #_ untuk translate
#
# class idea(models.Model):
#     _name = 'idea.nilai'
#     description = 'class untuk berlatih ttg input nilai di khs'
#
#     name = fields.Char('Number', size=64, required=True, index=True, readonly=True,
#                        states={'draft': [('readonly', False)]})  # kita harus punya field name ini.
#
#     mhs_id = fields.Many2one('idea.khs', string='Mahasiswa', readonly=True, ondelete="cascade",
#                               states={'draft': [('readonly', False)]},
#                               domain="[('state', '=', 'done'), ('active','=','True')]")
#     matkul = fields.Char('Mata Kuliah', size=64, required=True, index=True, readonly=True,
#                        states={'draft': [('readonly', False)]})  # kita harus punya field name ini.
#
#     final_score = fields.Selection([('A', "A"), ('B+', "B"), ('B', "B"), ('C+', "C+"), ('C', "C"), ('D', "D")], readonly=False,
#                             default='draft')
#
#     date = fields.Date('Date Release', default=fields.Date.context_today, readonly=True,
#                        states={'draft': [('readonly', False)]})
#
#     state = fields.Selection(
#         [('done', 'Done'), ('draft', 'Draft'), ('canceled', 'Canceled')], 'State', readonly=True, default='draft')
#
#     def action_done(self):  # approve
#         self.state = 'done'
#
#     def action_canceled(self):
#         self.state = 'canceled'
#
#     def action_settodraft(self):
#         self.state = 'draft'
#
