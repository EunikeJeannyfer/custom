from odoo import models, fields, api, _
from openerp.exceptions import UserError
    #from odoo yg digunakan adalah u working directory
    #_ untuk translate

class kembali(models.Model): #inherit dari Model -> ini nama class sesuai python
    _name = 'perpus.kembali' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    description = 'class untuk mencatat pengembalian buku'
    # _rec_name = 'name' #default-nya name, ini untuk memberi tahu field mana yang jadi rec_name.
    # _order = 'date desc'

    #membuat attribute field

    name = fields.Char('Kode Pengembalian', size=64, required=True, index=True, readonly=True, states={'draft': [('readonly', False)]})
    pinjam_id = fields.Many2one('perpus.pinjam', string='Peminjaman', readonly=True, ondelete="cascade",
                              states={'draft': [('readonly', False)]},
                              domain="[('state', '=', 'done'), ('total_kembali', '=', '0')]")
                                #kode pinjam tidak bisa dikembalikan double (tergantung total kembali)

    date = fields.Date('Tgl Kembali', default=fields.Date.context_today, readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection(
        [('done', 'Done'),
         ('draft', 'Draft'), ('canceled', 'Canceled')], 'State', readonly=True, required=True, default='draft')
    _sql_constraints = [('name_unik', 'unique(name)', _('Kode Pengembalian must be unique!'))]

    def action_done(self):  #approve
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    @api.model_create_multi
    def create(self, vals_list):
        seq=self.env['ir.sequence'].search([("code", "=", "perpus.kembali")])
        if not seq:
            raise UserError(_("perpus.kembali sequence not found, please create idea.voting sequnce"))

        for val in vals_list:
            val['name'] = seq.next_by_id(sequence_date=val['date'])
                #name adalah field yang mau dikasih penomoran otomatis
        return super(kembali, self).create(vals_list)
        # self.name= seq.next_by_id(sequence_date=)