odoo.define('eloapps_solde_compte.ReportWidget', function(require) {
    'use strict';

    var core = require('web.core');
    var Widget = require('web.Widget');

    var QWeb = core.qweb;

    // hierarchie entre classes/chapitres/comptes
    // cette variable est formé comme suite :
    // - chaque ligne deplier est une clé du dict
    //   qui contient un tableau des fils
    //   et chaque fils est une clé du dict
    //   qui contient un tableau vide
    // exemple :
    // on veu deplier la ligne 2 qui a comme fils 3, 4
    //      hierarchie[2] = [3, 4]
    //      hierarchie[3] = []
    //      hierarchie[4] = []
    // si la ligne 3 est deplier alor :
    //      hierarchie[3] = [5, 6, 7]
    //      hierarchie[5] = []
    //      hierarchie[6] = []
    //      hierarchie[7] = []
    // cette variable nous permet de retrouvé la trace des fils
    // et en meme temp une condition d'arret pour la
    // fonction recursive (_remove_lines) qui l'utilise
    var hierarchie = {};

    var ReportWidget = Widget.extend({
        events: {
            'click span.o_stock_reports_foldable': 'fold',
            'click span.o_stock_reports_unfoldable': 'unfold',
            'click .o_stock_reports_web_action': 'boundLink',
        },
        init: function(parent) {
            this._super.apply(this, arguments);
        },
        start: function() {
            QWeb.add_template("/eloapps_solde_compte/static/src/xml/l10n_dz_plan_comptable_report_line.xml");
            return this._super.apply(this, arguments);
        },
        // recupere les attribut passé dans xml
        // puis redirige vers le bon modele et record
        boundLink: function(e) {
            e.preventDefault();
            return this.do_action({
                type: 'ir.actions.act_window',
                res_model: $(e.target).data('res-model'),
                res_id: $(e.target).data('active-id'),
                views: [
                    [false, 'form']
                ],
                target: 'current'
            });
        },
        // des qu'on plier une ligne
        // supprime tout les fils existant
        // qui a comme parent active_id
        _remove_lines: function(active_id, fast_unfold_fold) {
            var self = this;

            var childs = hierarchie[active_id];
            if (childs.length == 0 && !fast_unfold_fold) {
                self.$('tr[data-id=' + active_id + ']').remove();
            } else
                for (var i = 0; i < childs.length; i++) {
                    self._remove_lines(childs[i], false);
                    self.$('tr[data-id=' + childs[i] + ']').remove();
                }

            return true;
        },
        // est applé lorsqu'on plie une ligne
        fold: function(e) {
            var active_id = $(e.target).parents('tr').find('td.o_stock_reports_foldable').data('id');
            this._remove_lines(active_id, true);

            $(e.target).parents('tr').find('td.o_stock_reports_foldable').attr('class', 'o_stock_reports_unfoldable ' + active_id); // Change the class, rendering, and remove line from model
            $(e.target).parents('tr').find('span.o_stock_reports_foldable').replaceWith(QWeb.render("unfoldable", { lineId: active_id }));
            $(e.target).parents('tr').toggleClass('o_stock_reports_unfolded');
        },
        autounfold: function(target, lot_name) {
            var self = this;
            var $CurretElement;
            $CurretElement = $(target).parents('tr').find('td.o_stock_reports_unfoldable');
            var active_id = $CurretElement.data('id');
            hierarchie[active_id] = [];
            var active_model_name = $CurretElement.data('model');
            var active_model_id = $CurretElement.data('model_id');
            var row_level = $CurretElement.data('level');
            var $cursor = $(target).parents('tr');

            // recupere les fils direct du active_id
            // fils = group_ids et account_ids lié au active_id
            // active_id : la ligne qu'on veut deplier
            this._rpc({
                    model: 'l10n_dz.plan_comptable',
                    method: 'get_lines',
                    args: [parseInt(active_id, 10)],
                    kwargs: {
                        'model_id': active_model_id,
                        'model_name': active_model_name,
                        'level': parseInt(row_level) + 30 || 1
                    },
                })
                .then(function(lines) { // After loading the line
                    _.each(lines, function(line) { // Render each line
                        hierarchie[active_id].push(line.id);
                        hierarchie[line.id] = [];
                        // avoir 2 apré la virgule pour les champs
                        line.columns[2] = line.columns[2].toFixed(2).toString(); // debit
                        line.columns[3] = line.columns[3].toFixed(2).toString(); // credit
                        line.columns[4] = line.columns[4].toFixed(2).toString(); // solde (debit-credit)

                        // applique les changement sur la vue
                        $cursor.after(QWeb.render("report_plan_comptable_line", { l: line }));
                        // passé a la ligne suivante
                        $cursor = $cursor.next();

                        // enlever l'ouverture automatique des fils
                        // if ($cursor && line.unfoldable && line.lot_name == lot_name) {
                        //     self.autounfold($cursor.find(".fa-caret-right"), lot_name);
                        // }
                    });
                });
            $CurretElement.attr('class', 'o_stock_reports_foldable ' + active_id); // Change the class, and rendering of the unfolded line
            $(target).parents('tr').find('span.o_stock_reports_unfoldable').replaceWith(QWeb.render("foldable", { lineId: active_id }));
            $(target).parents('tr').toggleClass('o_stock_reports_unfolded');
        },
        // est applé lorqu'on deplie une ligne
        unfold: function(e) {
            this.autounfold($(e.target));
        },

    });

    return ReportWidget;

});