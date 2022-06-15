from odoo import models, fields, api, _
#from odoo yg digunakan adalah u working directory
#_ untuk translate

class merk(models.Model): #inherit dari Model -> ini nama class sesuai python
    _name = 'supermarket.merk' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    description = 'class untuk mencatat data merk'
    # _rec_name = 'name' #default-nya name, ini untuk memberi tahu field mana yang jadi rec_name.
    # _order = 'date desc'

    #membuat attribute field

    name = fields.Char('Merk', size=64, required=True, index=True, readonly=True, states={'draft': [('readonly', False)]})
    kode_merk = fields.Char('Kode Merk', size=64, required=True, index=True, readonly=True,
                      states={'draft': [('readonly', False)]})
    state = fields.Selection(
        [('done', 'Done'),
         ('draft', 'Draft'), ('canceled', 'Canceled')], 'State', readonly=True, required=True, default='draft')

    _sql_constraints = [('name_unik', 'unique(name)', _('Judul Buku must be unique!'))]

    def action_done(self):  #approve
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'




