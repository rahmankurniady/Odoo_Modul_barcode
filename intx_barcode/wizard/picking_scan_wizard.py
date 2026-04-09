from odoo import models, fields, api
from odoo.exceptions import UserError


class PickingScanWizard(models.TransientModel):
    _name = 'picking.scan.wizard'
    _description = 'Scan Barcode Wizard'

    picking_id = fields.Many2one('stock.picking')
    barcode = fields.Char("Scan Barcode", autofocus=True)
    qty = fields.Float("Qty", default=1)

    scan_line_ids = fields.Many2many(
        'stock.picking.scan.line',
        'picking_id',
        string='Scanned Items',
        readonly=True
    )
    
    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        picking_id = self.env.context.get('default_picking_id')

        if picking_id:
            res['picking_id'] = picking_id

            picking = self.env['stock.picking'].browse(picking_id)

            # 🔥 LOAD DATA KE WIZARD
            res['scan_line_ids'] = [(6, 0, picking.scan_line_ids.ids)]

        return res
        
    def action_scan(self):
        if not self.barcode:
            return

        product = self.env['product.product'].search([
            ('barcode', '=', self.barcode)
        ], limit=1)

        if not product:
            raise UserError(f"Barcode tidak ditemukan: {self.barcode}")

        if self.qty <= 0:
            raise UserError("Qty harus lebih dari 0")
        
        allowed_products = self.picking_id.move_ids.product_id

        # VALIDASI UTAMA
        if product not in allowed_products:
            raise UserError(f"Produk {product.display_name} tidak ada di Request!")
        
        # ambil move sesuai produk
        move = self.picking_id.move_ids.filtered(lambda m: m.product_id.id == product.id)

        if not move:
            raise UserError(f"Produk {product.display_name} tidak ditemukan di picking")

        # total qty yang diminta
        requested_qty = sum(move.mapped('product_uom_qty'))

        # qty yang sudah discan sebelumnya
        existing_line = self.env['stock.picking.scan.line'].search([
            ('picking_id', '=', self.picking_id.id),
            ('product_id', '=', product.id)
        ], limit=1)

        scanned_qty_existing = existing_line.scanned_qty if existing_line else 0

        # total jika ditambah scan sekarang
        total_after_scan = scanned_qty_existing + self.qty

        # VALIDASI OVER QTY
        if total_after_scan > requested_qty:
            raise UserError(
                f"Qty melebihi permintaan!\n"
                f"Diminta: {requested_qty}\n"
                f"Sudah discan: {scanned_qty_existing}\n"
                f"Scan sekarang: {self.qty}"
            )

        picking = self.picking_id

        line = self.env['stock.picking.scan.line'].search([
            ('picking_id', '=', self.picking_id.id),
            ('product_id', '=', product.id)
        ], limit=1)

        if line:
            line.scanned_qty += self.qty
        else:
            self.env['stock.picking.scan.line'].create({
                'picking_id': self.picking_id.id,
                'product_id': product.id,
                'scanned_qty': self.qty
            })

        # recompute
        picking._compute_scan_state()

        # 🔥 update list tanpa reload
        self.scan_line_ids = [(6, 0, picking.scan_line_ids.ids)]

        # reset input
        self.barcode = False
        self.qty = 1

        # reload wizard
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'picking.scan.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }

    