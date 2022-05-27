from odoo import models, fields, api, _
from odoo.exceptions import UserError

from datetime import datetime, timedelta

#from odoo yg digunakan adalah u working directory
#_ untuk translate

class pinjam(models.Model): #inherit dari Model -> ini nama class sesuai python
    _name = 'perpus.pinjam' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    description = 'class untuk mencatat peminjaman buku'
    # _rec_name = 'name' #default-nya name, ini untuk memberi tahu field mana yang jadi rec_name.
    # _order = 'date desc'

    #membuat attribute field

    name = fields.Char('Kode Peminjaman', size=64, required=True, index=True, readonly=True, default='new', states={})
    # name = fields.Char(compute="_compute_name", store=True, recursive=True)
    anggota_id = fields.Many2one('perpus.anggota', string='Peminjam', readonly=True, ondelete="cascade",
                                 states={'draft': [('readonly', False)]},
                                 domain="[('state', '=', 'done')]")
    buku_id = fields.Many2one('perpus.buku', string='Judul Buku', readonly=True, ondelete="cascade",
                              states={'draft': [('readonly', False)]},
                              domain="[('state', '=', 'done'), ('sisa_buku', '>', '0')]")
    date_pinjam = fields.Date('Tgl Pinjam', default=fields.Date.context_today, readonly=True, states={'draft': [('readonly', False)]})
    date_kembali = fields.Date('Tgl Kembali', readonly=True, states={'draft': [('readonly', False)]})
    cek_kembali = fields.Boolean('Kembali', default=False, readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection([('done', 'Done'), ('draft', 'Draft'), ('canceled', 'Canceled')],
                             'State', readonly=True, required=True, default='draft')
    _sql_constraints = [('name_unik', 'unique(name)', _('Kode Peminjaman must be unique!'))]

    #UNTUK RELASI KE MODEL KEMBALI
        #CEK, apakah buku belum dikembalikan
    kembali_ids = fields.One2many('perpus.kembali', 'pinjam_id', string='Pengembalian')
    total_kembali = fields.Integer("Kembali", compute="_compute_kembali", store=True, default=0)
    #date_kembali2 = fields.One2many('perpus.kembali', 'date', default='-')

    # @api.depends('s.buku_id', 'anggota_id')
    # # api depends --> dijalankan saat ada berubah ttg 3 hal diatas
    # def _compute_name(self):
    #     for s in self:
    #         s.name = "%s - %s" % (s.buku_id, s.anggota_id)
    #         # s = string, gaboleh yang lain. Kalau i integer

    # .filtered(lambda s: s.state == 'done')
    @api.depends("kembali_ids", "kembali_ids.state")
        #akan di cek ketika ada perubahan pada kembali_ids
    def _compute_kembali(self):
        for pinjam in self.filtered(lambda i: i.state == 'done'):
            val = { "total_kembali": 0 }
            for rec in pinjam.kembali_ids:
                if(rec.state == 'done'):
                    val["total_kembali"] += 1
                    pinjam.cek_kembali = True
                else:
                    pinjam.total_kembali= 0
                    pinjam.cek_kembali = False

            pinjam.update(val)

    def action_done(self):  #approve
        self.state = 'done'
        if self.name == 'new' or not self.name:
            seq = self.env['ir.sequence'].search([("code", "=", "perpus.pinjam")])
            if not seq:
                raise UserError(_("perpus.pinjam sequence not found, please create idea.idea sequence"))
            self.name = seq.next_by_id(sequence_date=self.date)
    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'
