from odoo import models, fields, api, _
#from odoo yg digunakan adalah u working directory
#_ untuk translate

class penjualan(models.Model): #inherit dari Model -> ini nama class sesuai python
    _name = 'supermarket.penjualan' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    description = 'class untuk mencatat data penjualan'
    # _rec_name = 'name' #default-nya name, ini untuk memberi tahu field mana yang jadi rec_name.
    # _order = 'date desc'

    #membuat attribute field

    name = fields.Char('Kode Penjualan', size=64, required=True, index=True, readonly=True, default="New",
                       states={'draft': [('readonly', True)]})
    # kode_penjualan = fields.Char('Kode Penjualan', size=64, required=True, index=True, readonly=False, default="New",
    #                              states={'draft': [('readonly', False)]})
    date = fields.Date('Tgl Transaksi', default=fields.Date.context_today, readonly=True,
                       states = {'draft': [('readonly', False)]})

    member_ids = fields.Many2one('res.partner', string='Customer', readonly=True, ondelete="cascade",
                                 states={'draft': [('readonly', False)]})
    total_transaksi = fields.Integer("Total Transaksi", compute="_compute_total_transaksi", store=True, default=0)
    state = fields.Selection(
        [('done', 'Done'), ('draft', 'Draft'), ('canceled', 'Canceled')],
        'State', readonly=True, required=True, default='draft')

    detailpenjualan_ids = fields.One2many('supermarket.detailpenjualan', 'penjualan_id')
            # domain="[('state', '=', 'done')]")

    _sql_constraints = [('name_unik', 'unique(name)', _('Judul Buku must be unique!'))]

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('supermarket.penjualan')
        return super(penjualan, self).create(vals)

    def action_done(self):  #approve
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    @api.depends('detailpenjualan_ids', 'detailpenjualan_ids.state')
    def _compute_total_transaksi(self):
        for penjualan in self.filtered(lambda i:i.state == 'done'):
            val = {"total_transaksi": 0}
            for rec in penjualan.detailpenjualan_ids:
                if (rec.state == 'done'):
                    val["total_transaksi"] += rec.jumlah

            val["total_transaksi"] += val["total_transaksi"] * 0.1
            penjualan.update(val)

    def action_wiz_penjualan(self):
        return {
            'type': 'ir.actions.act_window',    #return window
            'name': _('Wizard Penjualan'),
            'res_model': 'wiz.supermarket.penjualan',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_id': self.id},
        }

# class detailPenjualan(models.Model): #inherit dari Model -> ini nama class sesuai python
#     _name = 'supermarket.detailpenjualan' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
#     description = 'class untuk mencatat data detail penjualan'
#
#     #membuat attribute field
#
#     name = fields.Char('ID Detail Penjualan', size=64, required=True, index=True, readonly=True, default="New",
#                        states={'draft': [('readonly', False)]})
#     penjualan_id = fields.Many2one('supermarket.penjualan', string='Penjualan', ondelete="cascade")
#     produk_id = fields.Many2one('supermarket.produk', string='Produk', ondelete="cascade")
#     harga = fields.Integer("Harga @pcs", related='produk_id.harga')
#     pcs = fields.Integer('pcs', default=0 )
#     jumlah = fields.Integer('Total', compute="_compute_jumlah_harga", store=True, default=0)
#
#     _sql_constraints = [('name_unik', 'unique(name)', _('ID Detail must be unique!'))]
#
#     @api.depends("produk_id", "pcs")
#     def _compute_jumlah_harga(self):
#         valj = {"jumlah": 0}
#         a = detailPenjualan.harga * detailPenjualan.pcs
#         valj["jumlah"] = a
#
#         penjualan.update(valj)
#
#
#
