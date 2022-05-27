# from odoo import models, fields, api, _
# #from odoo yg digunakan adalah u working directory
# #_ untuk translate
#
# class idea(models.Model):
#     _name = 'idea.khs'
#     description = 'class untuk berlatih ttg khs'
#
#     name = fields.Char('Mahasiswa', size=64, required=True, index=True, readonly=True,
#                        states={'draft': [('readonly', False)]})  # kita harus punya field name ini.
#     semester = fields.Selection([('ganjil', "Ganjil"), ('genap', "Genap")], readonly=False,
#                        default='draft')
#         #fields.Char('Hallo', size=64, required=True, index=True, readonly=True,
#          #              states={'draft': [('readonly', False)]})  # kita harus punya field name ini.
#
#     tahun_ajaran = fields.Char('Tahun Ajaran', size=64, required=True, index=True, readonly=True,
#                        states={'draft': [('readonly', False)]})
#     date = fields.Date('Date Release', default=fields.Date.context_today, readonly=True,
#                        states={'draft': [('readonly', False)]})
#     state = fields.Selection(
#         [('done', 'Done'), ('draft', 'Draft'), ('canceled', 'Canceled')], 'State', readonly=True, default='draft')
#
#     ips = fields.Integer('IPS', readonly=True, states={'draft': [('readonly', False)]})
#
#     def action_done(self):  #approve
#         self.state = 'done'
#
#     def action_canceled(self):
#         self.state = 'canceled'
#
