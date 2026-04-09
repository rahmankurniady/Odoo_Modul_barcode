from odoo import models, fields, api


class StockPickingScanLine(models.Model):
    _name = 'stock.picking.scan.line'
    _description = 'Picking Scan Line'

    picking_id = fields.Many2one(
        'stock.picking',
        string='Picking',
        required=True,
        ondelete='cascade'
    )

    product_id = fields.Many2one(
        'product.product',
        string='Product',
        required=True
    )

    scanned_qty = fields.Float(
        string='Scanned Qty',
        default=1.0
    )

    demand_qty = fields.Float(
        string="Demand",
        compute="_compute_demand_qty",
        store=False
    )

    # Optional: untuk grouping
    barcode = fields.Char(string='Barcode')

    # ==========================
    # AUTO MERGE QTY
    # ==========================
    @api.model
    def create(self, vals):
        existing = self.search([
            ('picking_id', '=', vals.get('picking_id')),
            ('product_id', '=', vals.get('product_id')),
        ], limit=1)

        if existing:
            existing.scanned_qty += vals.get('scanned_qty', 1)
            return existing

        return super().create(vals)
    
    def _compute_demand_qty(self):
        for line in self:
            picking = line.picking_id
            product = line.product_id

            move = picking.move_ids.filtered(
                lambda m: m.product_id == product
            )

            line.demand_qty = sum(move.mapped('product_uom_qty'))