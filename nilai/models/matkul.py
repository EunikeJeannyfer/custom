from odoo import models, fields, api, _
#from odoo yg digunakan adalah u working directory
#_ untuk translate

class matkul(models.Model): #inherit dari Model -> ini nama class sesuai python
    _name = 'nilai.matkul' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    description = 'class untuk membuat daftar matkul'

    name = fields.Char('Nama MK', size=64, required=True, index=True, readonly=True, states={'draft': [('readonly', False)]})
    kode_mk = fields.Char('Kode MK', size=64, required=True, index=True, readonly=True,
                      states={'draft': [('readonly', False)]})

    sks = fields.Integer('SKS', default=0, readonly=True, states={'draft': [('readonly', False)]})
    active = fields.Boolean('Active', default=True, readonly=True, states={'draft': [('readonly', False)]})

    state = fields.Selection([('done', 'Done'), ('draft', 'Draft'), ('canceled', 'Canceled')], 'State', required=True,
                             default='draft', readonly=True)

    def action_done(self):  #approve
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'
