# -*- encoding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging as log
from math import ceil


class ConfigTimbre(models.Model):
    _name = 'config.timbre'
    _description = "Configuration Timbre Fiscal"

    name = fields.Char(
        string="Nom",
        required=True
    )

    tranche = fields.Float(
        string="Tranche",
        required=True,
        default=100,  # Default tranche for stamp duty
        help="Valeur utilisée pour calculer les tranches. Doit être strictement supérieure à zéro."
    )

    prix_1 = fields.Float(
        string="Prix tranche 1 (1 DA)",
        required=True,
        default=1.0,
        help="Prix pour la première tranche."
    )

    prix_2 = fields.Float(
        string="Prix tranche 2 (1.5 DA)",
        required=True,
        default=1.5,
        help="Prix pour la deuxième tranche."
    )

    prix_3 = fields.Float(
        string="Prix tranche 3 (2 DA)",
        required=True,
        default=2.0,
        help="Prix pour la troisième tranche."
    )

    mnt_min = fields.Float(
        string="Montant minimal",
        required=True,
        default=300.0,  # Default minimum amount for duty
        help="Montant minimum en dessous duquel aucun timbre n'est appliqué."
    )

    mnt_max_1 = fields.Float(
        string="Montant maximum tranche 1",
        required=True,
        default=30000.0,  # Upper bound for first tier
        help="Montant maximum pour la première tranche."
    )

    mnt_max_2 = fields.Float(
        string="Montant maximum tranche 2",
        required=True,
        default=100000.0,  # Upper bound for second tier
        help="Montant maximum pour la deuxième tranche."
    )

    montant_minimum_timbre = fields.Float(
        string="Timbre minimum",
        required=True,
        default=5.0,  # Minimum stamp duty
        help="Montant minimum de timbre fiscal appliqué."
    )

    sale_timbre = fields.Many2one(
        comodel_name='account.account',
        string="Compte contrepartie vente",
        help="Compte comptable utilisé pour les ventes."
    )

    purchase_timbre = fields.Many2one(
        comodel_name='account.account',
        string="Compte contrepartie achat",
        help="Compte comptable utilisé pour les achats."
    )

    montant_en_lettre = fields.Boolean(
        string="Afficher le montant en lettres sur l’impression des factures",
        help="Permet d'afficher le montant en lettres sur les factures."
    )

    @api.model
    def _timbre(self, montant):
        """
        Calculate stamp duty based on the updated law.
        """
        # if montant < self.mnt_min:
        #     log.warning("Montant inférieur au minimum, pas de timbre appliqué.")
        #     return 0.0

        # if not self.tranche or self.tranche <= 0:
        #     raise UserError(_("La valeur de 'tranche' doit être strictement supérieure à zéro. Vérifiez la configuration."))

        # Initialize stamp duty
        montant_avec_timbre = 0.0
        
        config_timbre_id  = self.env['config.timbre'].search([], limit=1)
        
        if config_timbre_id.mnt_min <= montant <= config_timbre_id.mnt_max_1:
            montant_avec_timbre = ceil(montant / config_timbre_id.tranche) * config_timbre_id.prix_1
        elif config_timbre_id.mnt_max_1 < montant <= config_timbre_id.mnt_max_2:
            montant_avec_timbre = ceil(montant / config_timbre_id.tranche) * config_timbre_id.prix_2
        elif montant > config_timbre_id.mnt_max_2:
            montant_avec_timbre = ceil(montant / config_timbre_id.tranche) * config_timbre_id.prix_3

        # Ensure minimum stamp duty is applied
        if montant_avec_timbre < config_timbre_id.montant_minimum_timbre:
            montant_avec_timbre = config_timbre_id.montant_minimum_timbre

        return montant_avec_timbre

    @api.onchange('tranche', 'prix_1', 'prix_2', 'prix_3', 'mnt_min', 'mnt_max_1', 'mnt_max_2')
    def check_negative_values(self):
        """
        Prevent negative values for numeric fields.
        """
        for record in self:
            if record.tranche < 0:
                record.tranche = abs(record.tranche)
            if record.prix_1 < 0:
                record.prix_1 = abs(record.prix_1)
            if record.prix_2 < 0:
                record.prix_2 = abs(record.prix_2)
            if record.prix_3 < 0:
                record.prix_3 = abs(record.prix_3)
            if record.mnt_min < 0:
                record.mnt_min = abs(record.mnt_min)
            if record.mnt_max_1 < 0:
                record.mnt_max_1 = abs(record.mnt_max_1)
            if record.mnt_max_2 < 0:
                record.mnt_max_2 = abs(record.mnt_max_2)

    @api.constrains('tranche', 'mnt_min', 'mnt_max_1', 'mnt_max_2')
    def _check_values(self):
        """
        Add constraints to ensure the validity of numeric fields.
        """
        for record in self:
            if record.tranche <= 0:
                raise ValidationError(_("La valeur de 'tranche' doit être strictement supérieure à zéro."))
            if record.mnt_min < 0:
                raise ValidationError(_("Le montant minimum doit être positif."))
            if record.mnt_max_1 <= record.mnt_min:
                raise ValidationError(_("Le montant maximum tranche 1 doit être supérieur au montant minimum."))
            if record.mnt_max_2 <= record.mnt_max_1:
                raise ValidationError(_("Le montant maximum tranche 2 doit être supérieur au montant maximum tranche 1."))
