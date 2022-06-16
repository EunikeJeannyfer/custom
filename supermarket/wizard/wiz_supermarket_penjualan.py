from odoo import models, fields, api, _
#from odoo yg digunakan adalah u working directory
#_ untuk translate

class wizdetail(models.TransientModel): #inherit dari Model -> ini nama class sesuai python
    _name = 'wiz.supermarket.penjualan' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    description = 'class untuk mencatat data penjualan'

    penjualan_id = fields.Many2one('supermarket.penjualan', string="Penjualan")
    date = fields.Date(related='penjualan_id.date')
    member_ids = fields.Many2one(related='penjualan_id.member_ids')
    produk_id = fields.Many2one('supermarket.produk', string='Produk', ondelete="cascade",
                                domain="[('state', '=', 'done'), ('stok', '>', '0')]")
    harga = fields.Integer(related='produk_id.harga')
    pcs = fields.Integer('pcs', default=0)
    jumlah = fields.Integer('Total', default=0, readonly=True)
    ref_kelas_lines_id = fields.Many2one('supermarket.detailpenjualan')

    # member_ids = fields.Many2one('res.partner', string='Customer', readonly=True, ondelete="cascade",
    #                              states={'draft': [('readonly', False)]})
    # produk_id = fields.Many2one(related='penjualan_id.produk_id')
    # harga = fields.Integer(related='penjualan_id.harga')
    # pcs = fields.Integer(related='penjualan_id.pcs')
    # jumlah = fields.Integer(related='penjualan_id.jumlah')

    # line_ids = fields.One2many('wiz.supermarket.penjualan.lines','wiz_header_id', string='Penjualan')

    def action_confirm(self):
        #disini mau passing grade yg diisi di wizard ke class kelas
        for rec in self:
            rec.ref_kelas_lines_id.produk_id = rec.produk_id
            rec.ref_kelas_lines_id.harga = rec.harga
            rec.ref_kelas_lines_id.pcs = rec.pcs
            rec.ref_kelas_lines_id.jumlah = rec.jumlah

    @api.model
    #agar ketika si wizard bisa ambil data parent default
    def default_get(self, fields_list):
        res=super(wizdetail,self).default_get(fields_list)
        res['penjualan_id'] = self.env.context['active_id']
        return res

    # @api.onchange('penjualan_id')
    # def onchange_penjualan_id(self):
    #     if not self.penjualan_id:
    #         return
    #     line_ids = self.env['wiz.supermarket.penjualan.lines']
    #     for rec in self.penjualan_id.detailpenjualan_ids:                          #kelas_id punya field line_ids
    #         line_ids += self.env['wiz.supermarket.penjualan.lines'].new({
    #             'wiz_header_id' : self.id,
    #             'wiz_produk_id' : rec.produk_id.id,
    #             'wiz_pcs' : rec.pcs,
    #             'ref_kelas_lines_id': rec.id
    #         })
    #         #cara embuat record baru di m2m atau o2m
    #     self.line_ids = line_ids
#
class detail_lines_wiz(models.TransientModel):
    _name = 'wiz.supermarket.penjualan.lines'
    _description = 'class untuk menyimpan detail transaksi suatu penjualan'
    wiz_header_id = fields.Many2one('wiz.supermarket.penjualan', 'penjualan_id')
    wiz_produk_id = fields.Many2one('supermarket.produk', string='Produk', ondelete='restrict',
                                 states={'draft': [('readonly', False)]})
    wiz_pcs = fields.Integer('pcs', default=0, readonly=False)
    ref_kelas_lines_id = fields.Many2one('supermarket.detailpenjualan')


