from odoo import models, fields, api, _
#from odoo yg digunakan adalah u working directory
#_ untuk translate

class ResPartner(models.Model):
    _inherit = 'res.partner'

    date = fields.Date('Tgl Daftar', default=fields.Date.context_today, readonly=True)
    # states = {'draft': [('readonly', False)]}
