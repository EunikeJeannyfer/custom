from odoo import models, fields, api, _
#from odoo yg digunakan adalah u working directory
#_ untuk translate

class wizkelas(models.TransientModel): #inherit dari Model -> ini nama class sesuai python
    _name = 'wiz.nilai.kelas' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    description = 'class untuk mencatat data kelas'

    kelas_id = fields.Many2one('nilai.kelas', string="Kelas")
    semester = fields.Selection(related='kelas_id.semester')
    tahun = fields.Char(related='kelas_id.tahun_ajaran')
    mk_id = fields.Many2one(related='kelas_id.mk_id')
    line_ids = fields.One2many('wiz.nilai.kelas.lines','wiz_header_id', string='Nilai')

    def action_confirm(self):
        #disini mau passing grade yg diisi di wizard ke class kelas
        for rec in self.line_ids:
            rec.ref_kelas_lines_id.grade = rec.grade

    @api.model
    #agar ketika si wizard bisa ambil data parent default
    def default_get(self, fields_list):
        res=super(wizkelas,self).default_get(fields_list)
        res['kelas_id'] = self.env.context['active_id']
        return res

    @api.onchange('kelas_id')
    def onchange_kelas_id(self):
        if not self.kelas_id:
            return
        line_ids = self.env['wiz.nilai.kelas.lines']
        for rec in self.kelas_id.line_ids:      #kelas_id punya field line_ids
            line_ids += self.env['wiz.nilai.kelas.lines'].new({
                'wiz_header_id' : self.id,
                'wiz_mhs_id' : rec.mhs_id.id,
                'ref_kelas_lines_id': rec.id
            })
            #cara embuat record baru di m2m atau o2m
        self.line_ids = line_ids

class kelas_lines_wiz(models.TransientModel):
    _name = 'wiz.nilai.kelas.lines'
    _description = 'class untuk menyimpan data nilai suatu kelas'
    wiz_header_id = fields.Many2one('wiz.nilai.kelas', string='Kelas')
    wiz_mhs_id = fields.Many2one('nilai.mahasiswa', string='Mahasiswa', ondelete='restrict')
    ref_kelas_lines_id = fields.Many2one('nilai.kelas.lines')
    grade = fields.Selection([('A','A'),
                                  ('B+','B+'),
                                  ('B','B'),
                                  ('C+','C+'),
                                  ('C','C'),
                                  ('D','D'),
                                  ('E','E'),
                                  ])
