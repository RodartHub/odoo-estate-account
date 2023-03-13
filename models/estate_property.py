from odoo import models

class EstateProperty(models.Model):
    
    # ---------------------------------------- Private Attributes ---------------------------------

    _inherit = 'estate_property'

    # ---------------------------------------- Action Methods -------------------------------------


    def action_sold(self):
        res=super(EstateProperty,self).property_status_sold()

        journal = self.env["account.move"].with_context(default_move_type="out_invoice")._get_default_journal()

        for prop in self:
            self.env["account.move"].create(
                {
                    "partner_id": prop.buyer_id.id,
                    "move_type": "out_invoice",
                    "journal_id": journal.id,
                    "invoice_line_ids": [
                        (
                            0,
                            0,
                            {
                                "name": prop.name,
                                "quantity": 1.0,
                                "price_unit": prop.selling_price * 6.0 / 100.0,
                            },
                        ),
                        (
                            0,
                            0,
                            {
                                "name": "Administrative fees",
                                "quantity": 1.0,
                                "price_unit": 100.0,
                            },
                        ),
                    ],
                }
            )

        return res
    
    
    
