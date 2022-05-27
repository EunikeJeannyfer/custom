from odoo import models, fields, api, _
#from odoo yg digunakan adalah u working directory
#_ untuk translate

class idea(models.Model): #inherit dari Model -> ini nama class sesuai python
    _name = 'idea.idea' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    description = 'class untuk berlatih ttg idea'
        # _rec_name = 'name' #default-nya name, ini untuk memberi tahu field mana yang jadi rec_name.
        # _order = 'date desc'
        # id = fields.Integer() ini otomatis ada di odoo, akan jadi PK

        # membuat attribute field. Field ini punya common parameter
        # field. ... adalah tipe data, misal field.integer field.Many2many dll

    name = fields.Char('Number', size=64, required=True, index=True, readonly=True, states={'draft': [('readonly', False)]})  # kita harus punya field name ini.
        #fungsi states= .... untuk mengatur ketika draft maka readonly = False
        #states = parameter, beda dgn state
        #string 'Number' ga perlu ditulis string= karena otomatis parameter pertama dr field adalah string

    date = fields.Date('Date Release', default=fields.Date.context_today, readonly=True,states={'draft': [('readonly', False)]})
    # att pertama selalu String shg tdk perlu ditulis nama parameter-nya

    state = fields.Selection(
        [('draft', 'Draft'),  # draft--> key, secara technical yang disimpan di dbase, Draft: value yang dilihat user
         ('confirmed', 'Confirmed'),
         ('done', 'Done'),
         ('canceled', 'Canceled')], 'State', required=True, readonly=True,  # krn required, sebaiknya dikasi default
        default='draft')  # tuple di dalam list, nama field harus state spy bisa diakses oleh states
    #harus ada field state, nama gaboleh ganti
    #readonly = True karena nnt ketika input data, ada yg tidak bisa diubah" lagi

    # Description is read-only when not draft!
    description = fields.Text('Description', readonly=True, states={'draft': [('readonly', False)]})
    active = fields.Boolean('Active', default=True, readonly=True, states={'draft': [('readonly', False)]})
    confirm_date = fields.Date('Confirm date')

    # by convention, many2one fields end with '_id'
    #ini relational field
    confirm_partner_id = fields.Many2one('res.partner', 'Confirm By', readonly=True)
        #states={'draft': [('readonly', False)]})
        #sponsor_ids = fields.Many2many('res.partner', 'idea_sponsor_rel', 'idea_id', 'sponsor_id','Sponsors')
        #res.partner adalah tabel dr odoo (ketika from odoo import ..)

    sponsor_ids = fields.Many2many('res.partner', string='Sponsors')
        #kalau ga define string = Sponsor, maka akan dibuat otomatis persis (SPONSOR_IDS) dlm upper case
    score = fields.Integer('Score', default=0, readonly=True)
        # 'Score' adalah string untuk nama kolom di odoo sprt Number di sales
    owner = fields.Many2one('res.partner', 'Owner', index=True, readonly=True, states={'draft': [('readonly', False)]})

    #VOTING
    voting_ids = fields.One2many('idea.voting', 'idea_id', string='Votes')
    total_yes = fields.Integer("Yes", compute="_compute_vote", store=True, default=0)
    total_no = fields.Integer("No", compute="_compute_vote", store=True, default=0)
    total_abstain = fields.Integer("Abstain", compute="_compute_vote", store=True, default=0)
    voter_id = fields.Many2one('res.users', 'Voted By', readonly=True, ondelete="cascade", default=lambda self: self.env.user)
    _sql_constraints = [('name_unik', 'unique(name)', _('Ideas must be unique!'))]

        # function yg dpnnya _ itu private function, mis : _compute_vote
        # _('Ideas...') _ untuk translate
    @api.depends("voting_ids", "voting_ids.vote", "voting_ids.state")
        #api depends ini bisa cek perubahan di UI dan program, @api.onchange gabisa
        #ini fungsinya supaya di cek perubahan pada voting_ids, voting_ids.vote voting_ids.state

    def _compute_vote(self):
        for idea in self.filtered(lambda i:i.state=='done'):
            val = {
                "total_yes" : 0,
                "total_no": 0,
                "total_abstain": 0
            }

            #for rec in idea.voting_ids:
            for rec in idea.voting_ids.filtered(lambda s:s.state=='voted'):
                if rec.vote == 'yes':
                    val["total_yes"] += 1
                elif rec.vote == 'no':
                    val["total_no"] += 1
                else:
                    val["total_abstain"] += 1
            idea.update(val)
        #lambda adalah sebuah fungsi untuk mengirimkan s (voting yg sudah voted)
    def action_done(self):  #approve
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_settodraft(self):
        self.state = 'draft'