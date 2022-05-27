from odoo import models, fields, api, _
#from odoo yg digunakan adalah u working directory
#_ untuk translate

class kelas(models.Model): #inherit dari Model -> ini nama class sesuai python
    _name = 'nilai.kelas' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    description = 'class untuk mencatat data kelas'
    # _rec_name = 'name' #default-nya name, ini untuk memberi tahu field mana yang jadi rec_name.
    # _order = 'date desc'

    #membuat attribute field

    name = fields.Char(compute ="_compute_name", store=True, recursive=True)
    semester = fields.Selection([ ('ganjil', "Ganjil"),
                                  ('genap', "Genap")], readonly=True,
                                default="Genap", states={'draft': [('readonly', False)]})
    tahun_ajaran = fields.Char('Tahun', size=15, default="2021/2022", required=True, index=True, readonly=True,
                               states={'draft': [('readonly', False)]})
    mk_id = fields.Many2one('nilai.matkul', string='Mata Kuliah', readonly=True, ondelete="cascade",
                             states={'draft': [('readonly', False)]},
                             domain="[('state', '=', 'done')]")
    line_ids = fields.One2many('nilai.kelas.lines', 'kelas_id', string='Nilai', readonly=True,
                               states={'draft': [('readonly', False)]})
    state = fields.Selection(
        [('done', 'Done'),
         ('draft', 'Draft'),
         ('canceled', 'Canceled')], 'State', readonly=True, required=True, default='draft')

    _sql_constraints = [('name_unik', 'unique(name)', _('Name must be unique!'))]


    @api.depends('mk_id.name', 'semester', 'tahun_ajaran')
        #api depends --> dijalankan saat ada berubah ttg 3 hal diatas
    def _compute_name(self):
        for s in self:
            s.name = "%s - %s - %s" % (s.mk_id.name, s.semester, s.tahun_ajaran)
            #s = string, gaboleh yang lain. Kalau i integer

    def action_done(self):  #approve
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    def action_wiz_nilai(self):
        return {
            'type': 'ir.actions.act_window',    #return window
            'name': _('Wizard Nilai Kelas'),
            'res_model': 'wiz.nilai.kelas',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_id': self.id},
        }

class kelas_lines(models.Model): #inherit dari Model -> ini nama class sesuai python
    _name = 'nilai.kelas.lines' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    description = 'class untuk mencatat data nilai suatu kelas'

    kelas_id = fields.Many2one('nilai.kelas', string="Kelas", ondelete="cascade" )
    mhs_id = fields.Many2one('nilai.mahasiswa', string="Mahasiswa", ondelete="restrict")
    grade = fields.Selection([('A','A'),
                              ('B+','B+'),
                              ('B','B'),
                              ('C+','C+'),
                              ('C','C'),
                              ('D','D'),
                              ('E','E'),
                              ])

    _sql_constraints = [('name_unik', 'unique(kelas_id, mhs_id)', _('The student is already exist!'))]

