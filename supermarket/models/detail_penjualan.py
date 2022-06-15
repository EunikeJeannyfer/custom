from odoo import models, fields, api, _
#from odoo yg digunakan adalah u working directory
#_ untuk translate

class detailPenjualan(models.Model): #inherit dari Model -> ini nama class sesuai python
    _name = 'supermarket.detailpenjualan' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    description = 'class untuk mencatat data detail penjualan'

    #membuat attribute field

    name = fields.Char('ID Detail Penjualan', size=64, required=True, index=True, readonly=True, default="New",
                       states={'draft': [('readonly', False)]})
    penjualan_id = fields.Many2one('supermarket.penjualan', string='Penjualan', readonly=True, ondelete="cascade",
                                   states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done')]")
    produk_id = fields.Many2one('supermarket.produk', string='Produk', ondelete="cascade", states={'draft': [('readonly', False)]},
                                domain="[('state', '=', 'done'), ('stok', '>', '0')]")
    stok = fields.Integer("Stok", related='produk_id.stok')
    harga = fields.Integer("Harga @pcs", related='produk_id.harga')
    # harga = fields.Integer("Harga @pcs", compute="_compute_harga", store=True, default=0)
    pcs = fields.Integer('pcs', default=0, states={'draft': [('readonly', False)]})
    jumlah = fields.Integer('Total', default=0, readonly=True, states={'draft': [('readonly', False)]})
    # jumlah = fields.Integer('Total', compute="_compute_jumlah_harga", store=True, default=0)

    state = fields.Selection(
        [('done', 'Done'),
         ('draft', 'Draft'), ('canceled', 'Canceled')], 'State', readonly=True, required=True, default='draft')

    _sql_constraints = [('name_unik', 'unique(name)', _('ID Detail must be unique!'))]

    def action_done(self):  #approve
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    # @api.onchange("produk_id", "produk_id.state")
    # def _compute_harga(self):
    #     for detailPenjualan in self.filtered(lambda i: i.state == 'done'):
    #         val = {"harga": 0}
    #
    #         for rec in detailPenjualan.produk_id:
    #             if (rec.state == 'done'):
    #                 self.harga += rec.harga
    #
    #         detailPenjualan.update(val)

    # @api.onchange("harga", "pcs")
    # def _compute_jumlah_harga(self):
    #     valj = {"jumlah": detailPenjualan.jumlah}
    #     a = detailPenjualan.harga * detailPenjualan.pcs
    #     valj["jumlah"] = a
    #
    #     detailPenjualan.update(jumlah)

    # @api.onchange("harga", "pcs")
    # def _compute_jumlah_harga(self):
    #     for detailPenjualan in self.filtered(lambda i: i.state == 'done'):
    #         val = {"jumlah": 0}
    #         for rec in self:
    #             if (rec.state == 'done'):
    #                 a = rec.harga * rec.pcs
    #                 val["jumlah"] = a
    #
    #         detailPenjualan.update(val)

