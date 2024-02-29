from odoo import api, models,fields, _

class SchoolModel(models.Model):
    _name = "school_model"
    _description = "List of students"

    first_name = fields.Char(string="first_name", required=True)
    middle_name = fields.Char(string="middle_name", required=True)
    last_name = fields.Char(string="last_name", required=True)
    student_photo = fields.Binary(string="student_photo", )
    student_age = fields.Integer(string="Student Age", required=True)
    student_dob = fields.Date(string="Date of start", )
    student_gender = fields.Selection([('m', 'Male'), ('f', 'Female'), ('o', 'Other')], string='Gender')
    student_blood_group = fields.Selection([('A+', 'A+ve'), ('B+', 'B+ve'), ('O+', 'O+ve'), ('AB+', 'AB+ve'),
    ('A-', 'A-ve'), ('B-', 'B-ve')], string='Blood Group')
    nationality = fields.Many2one('res.country', string='Nationality')
    ref = fields.Char(string="Reference", default=lambda self: _('New'))

    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['ref'] = self.env['ir.sequence'].next_by_code('school.student')
        return super(SchoolModel, self).create(vals_list)