# -*- coding: utf-8 -*-

#####################################################################
#
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
#####################################################################

from odoo import models, fields, api, _
import requests

# API KEY from deepl.com for using the translation engine
AUTH_KEY = '4ec5f1d9-e9db-887e-38ab-11df6e3237cf'

class EqProductTemplate(models.Model):
    _inherit = "product.template"

    product_translation_id = fields.Many2one('eq_product_translation', ondelete="cascade")
    en_name = fields.Char('Name (English)', related='product_translation_id.name')
    en_description_sale = fields.Char('Description (English)', related='product_translation_id.description_sale')

    def dispatch_translation_request(self, record):
        """

        Receives the record for translation from caller function and sends a POST request to deepl.com
        Record is received in JSON form, multiple records are appended into a list
        :return: english name with capital first letters, english description
        """

        en_name = ''
        en_desc = ''
        param = {'text': [record.name, record.description_sale], 'source_lang': 'DE', 'target_lang': 'EN',
                 'auth_key': AUTH_KEY}
        response = requests.post('https://api.deepl.com/v2/translate?', data=param)
        if response.status_code == 200:
            try:
                en_name = response.json()['translations'][0].get('text', '')
                en_desc = response.json()['translations'][1].get('text', '')
            except IndexError:
                pass

        return en_name, en_desc

    @api.multi
    def translate_to_english(self):
        """

        Translates product name and description on click of 'Translate from German to English' button from action menu
        on product tree view or retrieves from database. The columns are appended to existing product.template tree view
        :return: product_template tree view, form view with product details
        """

        for record in self:
            if not record.product_translation_id:
                en_name, en_desc = self.dispatch_translation_request(record)
                new_rec = self.env['eq_product_translation'].create({'name': en_name.title(),
                                                                     'description_sale': en_desc})
                record.write({'product_translation_id': new_rec.id})

        view_id = self.env.ref('product.product_template_tree_view').id

        return {
            'name': _('Products Translated'),
            'domain': [('id', 'in', self.ids)],
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'product.template',
            'views': [(view_id, 'tree'), (False, 'form')],
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'auto_refresh': 1,
            'context': {'translated': True}
        }

class EqProductTranslation(models.Model):
    _name = 'eq_product_translation'


    product_id = fields.One2many('product,template', 'id', string='Product ID')
    name = fields.Char(string="Name (English)", index=True)
    description_sale = fields.Char(string="Description for Quotation (English)")