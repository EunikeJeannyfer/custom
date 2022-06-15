from odoo import models, fields, api, _
#from odoo yg digunakan adalah u working directory
#_ untuk translate

class produk(models.Model): #inherit dari Model -> ini nama class sesuai python
    _name = 'supermarket.produk' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    description = 'class untuk mencatat data merk'

    #membuat attribute field

    name = fields.Char(compute ="_compute_name", store=True, recursive=True)
    jenis_id = fields.Many2one('supermarket.jenis_produk', string='Jenis Produk', readonly=True, ondelete="cascade",
                               states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done')]")
    merk_id = fields.Many2one('supermarket.merk', string='Merk', readonly=True, ondelete="cascade",
                              states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done')]")
    variasi = fields.Char('Variasi', size=64, required=True, index=True, readonly=True,
                            states={'draft': [('readonly', False)]})
    kategori_id = fields.Many2one('supermarket.kategori_produk', string='Kategori', readonly=True, ondelete="cascade",
                                  states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done')]")

    harga = fields.Integer("Harga", compute="_compute_harga", store=True, default=0)
    stok = fields.Integer("Stok", compute="_compute_stok_produk", store=True, default=0)
    # sisa_stok = fields.Integer("Sisa Stok", compute="_compute_update_stok_produk", store=True, default=0)

    state = fields.Selection(
        [('done', 'Done'),
         ('draft', 'Draft'), ('canceled', 'Canceled')], 'State', readonly=True, required=True, default='draft')

    beli_ids = fields.One2many('supermarket.pembelian', 'produk_id', string='Pembelian')
    detail_ids = fields.One2many('supermarket.detailpenjualan', 'produk_id', string='Detail Penjualan')

    _sql_constraints = [('name_unik', 'unique(name)', _('Nama Produk must be unique!'))]

    @api.depends('jenis_id.name', 'merk_id.name', 'variasi')
    # api depends --> dijalankan saat ada berubah ttg 3 hal diatas
    def _compute_name(self):
        for s in self:
            s.name = "%s - %s - %s" % (s.merk_id.name, s.jenis_id.name, s.variasi)
            # s = string, gaboleh yang lain. Kalau i integer

    @api.depends('detail_ids', 'detail_ids.state', 'beli_ids', 'beli_ids.state')
    def _compute_stok_produk(self):
        for produk in self.filtered(lambda i:i.state == 'done'):
            val = {"stok": 0}
            for rec in produk.beli_ids:
                if (rec.state == 'done'):
                    val["stok"] += rec.pcs

            a = 0
            for rec in produk.detail_ids:
                if (rec.state == 'done'):
                    a += rec.pcs

            val["stok"] -= a
            produk.update(val)

    @api.depends('beli_ids', 'beli_ids.state')
    def _compute_harga(self):
        for produk in self.filtered(lambda i: i.state == 'done'):
            val = {"harga": 0}
            a = 0
            co = 1
            cek = True
            for rec in produk.beli_ids:
                if (rec.state == 'done'):
                    cek = False
                    co +=1
                    a += rec.harga_jual

            if cek == True:
                val["harga"] = a/co
            else:
                val["harga"] = a /(co-1)
            produk.update(val)

    def action_done(self):  #approve
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'


