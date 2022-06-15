from odoo import models, fields, api, _
#from odoo yg digunakan adalah u working directory
#_ untuk translate

class pembelian(models.Model): #inherit dari Model -> ini nama class sesuai python
    _name = 'supermarket.pembelian' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    description = 'class untuk mencatat data pembelian'

    #membuat attribute field

    name = fields.Char(compute ="_compute_name", store=True, recursive=True)
    kode_pembelian = fields.Char('Pembelian', size=64, required=True, index=True, readonly=True, states={'draft': [('readonly', False)]})
    produk_id = fields.Many2one('supermarket.produk', string='Produk', readonly=True, ondelete="cascade",
                                states={'draft': [('readonly', False)]})
    pcs = fields.Integer('pcs', default=0, readonly=True, states={'draft': [('readonly', False)]})
    harga_beli = fields.Integer('Harga Beli', default=0, readonly=True, states={'draft': [('readonly', False)]})
    harga_jual = fields.Integer('Harga Jual', default=0, readonly=True, states={'draft': [('readonly', False)]})

    state = fields.Selection(
        [('done', 'Done'),
         ('draft', 'Draft'), ('canceled', 'Canceled')], 'State', readonly=True, required=True, default='draft')

    _sql_constraints = [('name_unik', 'unique(name)', _('Judul Buku must be unique!'))]

    @api.depends('kode_pembelian', 'produk_id.name')
    # @api.depends('name')
    # api depends --> dijalankan saat ada berubah ttg 2 hal diatas
    def _compute_name(self):
        for s in self:
            s.name = "%s - %s" % (s.kode_pembelian, s.produk_id.name)
            # s = string, gaboleh yang lain. Kalau i integer

    def action_done(self):  #approve
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'






