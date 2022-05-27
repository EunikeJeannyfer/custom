from odoo import models, fields, api, _
#from odoo yg digunakan adalah u working directory
#_ untuk translate

class voting(models.Model): #inherit dari Model -> ini nama class sesuai python
    _name = 'idea.voting' #attribut dari class Model (lihat dokumen odoo) Modul.Model  jadi nama tabel (ini nama class/tabel sesuai odoo), jadi kalau akses data berdasarkan nama ini
    description = 'class untuk berlatih ttg voting di idea'
    # _rec_name = 'name' #default-nya name, ini untuk memberi tahu field mana yang jadi rec_name.
    # _order = 'date desc'

    #membuat attribute field

    name = fields.Char('Number', size=64, required=True, index=True, readonly=True, states={'draft': [('readonly', False)]})  # kita harus punya field name ini.
    date = fields.Date('Date Release', default=fields.Date.context_today, readonly=True,states={'draft': [('readonly', False)]})
    state = fields.Selection(
        [('voted', 'Voted'),
         ('draft', 'Draft'), ('canceled', 'Canceled')], 'State', readonly=True,  # krn required, sebaiknya dikasi default
        default='draft')

    #_sql_constraints = [('name_unik', 'unique(name)', _('Ideas must be unique!'))]

    vote = fields.Selection([('yes', "Yes"), ('no', "No"), ('abstain', "Abstain")], readonly=False,
                            default='draft')

    voter_id = fields.Many2one('res.users', 'Voted By', readonly=True, ondelete="cascade", default=lambda self: self.env.user)
    idea_id = fields.Many2one('idea.idea', string='Idea', readonly=True, ondelete="cascade", states={'draft': [('readonly', False)]},
                              domain="[('state', '=', 'done'), ('active','=','True')]")
        #ondelete ="restrict" jika master tidak boleh dihapus
        # ondelete="default" jika master dihapus maka menjadi null di database / false di phyton

    #related field
    idea_date = fields.Date("Idea date", related='idea_id.date')

    def action_voted(self):  #approve
        self.state = 'voted'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'