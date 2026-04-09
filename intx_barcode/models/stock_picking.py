from odoo import models, fields, api
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    scan_state = fields.Selection([
        ('not_scanned', 'Not Scanned'),
        ('partial', 'Partial'),
        ('complete', 'Complete')
    ], compute='_compute_scan_state', store=True)

    scan_line_ids = fields.One2many(
        'stock.picking.scan.line',
        'picking_id',
        string='Scan Lines'
    )

    # ==========================
    # COMPUTE SCAN STATE
    # ==========================
    @api.depends(
        'scan_line_ids.scanned_qty',
        'scan_line_ids.product_id',
        'move_ids_without_package.product_uom_qty',
        'move_ids_without_package.product_id'
    )
    def _compute_scan_state(self):
        for picking in self:
            if not picking.scan_line_ids:
                picking.scan_state = 'not_scanned'
                continue

            all_complete = True

            for move in picking.move_ids_without_package:
                scanned_qty = sum(
                    picking.scan_line_ids.filtered(
                        lambda l: l.product_id == move.product_id
                    ).mapped('scanned_qty')
                )

                if scanned_qty < move.product_uom_qty:
                    all_complete = False
                    break

            picking.scan_state = 'complete' if all_complete else 'partial'

    # ==========================
    # VALIDATION CONTROL
    # ==========================
    def button_validate(self):
        for picking in self:

            print("=== SCAN STATUS PICKING: ", picking.name,  " ===")

            for move in picking.move_ids_without_package:
                scanned_qty = sum(
                    picking.scan_line_ids.filtered(
                        lambda l: l.product_id.id == move.product_id.id
                    ).mapped('scanned_qty')
                )

                print(
                    "Product: ",move.product_id.display_name,
                    " | Demand: ",move.product_uom_qty,
                    " | Scanned: ",scanned_qty                    
                )

            print("FINAL SCAN STATE: ", picking.scan_state)

            if picking.move_ids_without_package and picking.scan_state != 'complete':
                raise UserError(
                    "Semua barang harus discan sebelum validasi!"
                )
        return super().button_validate()

    # ==========================
    # OPEN SCAN WIZARD
    # ==========================
    def action_open_scan_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'picking.scan.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_picking_id': self.id
            }
        }