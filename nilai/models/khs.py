from odoo import models, fields, api, _
#from odoo yg digunakan adalah u working directory
#_ untuk translate

class khs(models.Model): #inherit dari Model -> ini nama class sesuai python
    _name = 'nilai.khs' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    description = 'class untuk membuat khs'
    # _rec_name = 'name' #default-nya name, ini untuk memberi tahu field mana yang jadi rec_name.
    # _order = 'date desc'

    #membuat attribute field

    name = fields.Char(compute ="_compute_name", store=True, recursive=True)
        #compute defaultnya false, kalau mau true harus di setting
        #selain compute default store nya true
    mhs_id = fields.Many2one('nilai.mahasiswa', string='Mahasiswa', readonly=True, ondelete="cascade",
                             states={'draft': [('readonly', False)]},
                             domain="[('state', '=', 'done'), ('status','=','aktif')]")
    semester = fields.Selection([ ('ganjil', "Ganjil"), ('genap', "Genap")], readonly=False,
                                default='draft', states={'draft': [('readonly', False)]})
    tahun_ajaran = fields.Char('Tahun', size=64, default="2021/2022", required=True, index=True, readonly=True,
                        states={'draft': [('readonly', False)]})
    ips = fields.Float("IPS", compute="_compute_ips", default=0, store=True)

    state = fields.Selection(
        [('done', 'Done'),
         ('draft', 'Draft'), ('canceled', 'Canceled')], 'State', readonly=True,  # krn required, sebaiknya dikasi default
        default='draft')
    #nilai_mhs_ids =
    _sql_constraints = [('name_unik', 'unique(name)', _('KHS must be unique!'))]

    @api.depends('mhs_id.name', 'semester', 'tahun_ajaran')
        #api depends --> dijalankan saat ada berubah ttg 3 hal diatas
    def _compute_name(self):
        for s in self:
            s.name = "%s - %s - %s" % (s.mhs_id.name, s.semester, s.tahun_ajaran)
            #s = string, gaboleh yang lain. Kalau i integer

    def _compute_ips(self):
        self.ips = 0
        total_sks = 0
        for nilai_mhs in self.nilai_mhs_ids:
            self.ips+=nilai_mhs.subtotal
            total_sks+=nilai_mhs.sks
        if(total_sks==0):
            self.ips = 0
        else:
            self.ips =self.ips/total_sks

    def action_done(self):  #approve
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'
