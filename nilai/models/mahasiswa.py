from odoo import models, fields, api, _
#from odoo yg digunakan adalah u working directory
#_ untuk translate

class mahasiswa(models.Model): #inherit dari Model -> ini nama class sesuai python
    _name = 'nilai.mahasiswa' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    description = 'class untuk membuat daftar mahasiswa'
    # _rec_name = 'name' #default-nya name, ini untuk memberi tahu field mana yang jadi rec_name.
    # _order = 'date desc'

    #membuat attribute field

    name = fields.Char('NRP', size=64, required=True, index=True, readonly=True, states={'draft': [('readonly', False)]})
    nama_mhs = fields.Char('Nama', size=64, required=True, index=True, readonly=True,
                      states={'draft': [('readonly', False)]})

    angkatan = fields.Char('Angkatan', size=64, required=True, index=True, readonly=True, states={'draft': [('readonly', False)]})
    #total_ipk = buat hitungannya

    date = fields.Date('Date Masuk', default=fields.Date.context_today, readonly=True, states={'draft': [('readonly', False)]})
    status = fields.Selection([('aktif', "Aktif"), ('cuti', "Cuti"), ('keluar', "Keluar")], readonly=False)

    state = fields.Selection(
        [('done', 'Done'),
         ('draft', 'Draft'), ('canceled', 'Canceled')], 'State', readonly=True,  # krn required, sebaiknya dikasi default
        default='draft')

    def action_done(self):  #approve
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    def tes_bookrent(self):
        print("ini di mahasiswa")
        t = self.env.context.get('keterangan')
        print(t.keterangan)
