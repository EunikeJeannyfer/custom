from odoo import models, fields, api, _
#from odoo yg digunakan adalah u working directory
#_ untuk translate

class buku(models.Model): #inherit dari Model -> ini nama class sesuai python
    _name = 'perpus.buku' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    description = 'class untuk mencatat data buku'
    # _rec_name = 'name' #default-nya name, ini untuk memberi tahu field mana yang jadi rec_name.
    # _order = 'date desc'

    #membuat attribute field

    name = fields.Char('Judul Buku', size=64, required=True, index=True, readonly=True, states={'draft': [('readonly', False)]})
    kode_buku = fields.Char('Kode Buku', size=64, required=True, index=True, readonly=True,
                      states={'draft': [('readonly', False)]})
    pengarang = fields.Char('Pengarang', size=64, required=True, index=True, readonly=True,
                            states={'draft': [('readonly', False)]})
    kategori = fields.Many2one('perpus.kategori', string='Kategori', readonly=True, ondelete="cascade",
                               states={'draft': [('readonly', False)]},
                               domain="[('state', '=', 'done')]")
    date = fields.Date('Date Masuk', default=fields.Date.context_today, readonly=True,
                       states={'draft': [('readonly', False)]})
    jumlah_buku = fields.Integer('Jumlah Buku', default=0, readonly=True, states={'draft': [('readonly', False)]})

    state = fields.Selection(
        [('done', 'Done'),
         ('draft', 'Draft'), ('canceled', 'Canceled')], 'State', readonly=True, required=True, default='draft')

    _sql_constraints = [('name_unik', 'unique(name)', _('Judul Buku must be unique!'))]

    #PEMINJAMAN
    pinjam_ids = fields.One2many('perpus.pinjam', 'buku_id', string='Peminjaman')
    sisa_buku = fields.Integer("Sisa Buku", compute="_compute_sisa_buku", store=True, default=0)
    # anggota_id = fields.One2many('perpus.pinjam', 'anggota_id')
    #date_kembali = fields.One2many('perpus.pinjam', 'date_kembali2')


    @api.depends("pinjam_ids", "pinjam_ids.state", "pinjam_ids.buku_id", "pinjam_ids.total_kembali")
    def _compute_sisa_buku(self):
        for buku in self.filtered(lambda i: i.state == 'done'):
            val = { "sisa_buku": buku.jumlah_buku }
            for rec in buku.pinjam_ids.filtered(lambda s: s.state == 'done'):
                if rec.total_kembali == 0:              #if 1 artinya sudah dikembalikan
                    val["sisa_buku"] -= 1
                else:
                    val["sisa_buku"] -= 0

            buku.update(val)

    def action_tes(self):
        # self.env['res.partner']
        # akan muncul object
        # contoh ambil active user
        print(self.env.user.name)
        # #contoh ambil active company
        print(self.env.company.name)
        # #contoh common orm method search
        a = self.env["res.partner"].search([('name', 'ilike', 'Gemini')])
        # a = kumpulan object
        for rec in a:
            print(rec.name)
        a = self.env["res.partner"].search([], limit=2)
        # limit = 2 artinya 2 teratas

        # contoh context
        print(self.env.context.get('lang'))
        #
        t = self.env.context.copy()
        t['keterangan'] = 'Ideku'
        self.with_context(t).action_done()
        #
        b = self.env["nilai.mahasiswa"]
        b.with_context(t).tes_bookrent()

        #contoh query select
        query = "select name from res_partner order by name desc limit 3"
        self.env.cr.execute(query)
        res = self.env.cr.fetchall()
        for data in res:
            print(data[0])

        #contoh query update
        # query = "update idea_idea set state='done' where state in ('confirmed', 'draft')"

        #contoh browse
        query = "select * from res_partner limit 3"
        self.env.cr.execute(query)
        res = self.env['res.partner'].browse([row[0] for row in self.env.cr.fetchall()])
        for rec in res:
            print(rec.name)

    def action_done(self):  #approve
        self.state = 'done'
        t = self.env.context
        print(t.get('keterangan'))

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'


