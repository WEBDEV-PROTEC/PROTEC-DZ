odoo.define('eloapps_solde_compte.l10n_dz_report_tag', function(require) {
    'use strict';

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var session = require('web.session');
    var ReportWidget = require('eloapps_solde_compte.ReportWidget');
    var QWeb = core.qweb;

    var journals = [];
    var exercices = [];
    var periodes = [];

    var l10n_dz_report_tag = AbstractAction.extend({
        hasControlPanel: true,

        // Stores all the parameters of the action.
        init: function(parent, action) {
            this.actionManager = parent;
            this.given_context = Object.assign({}, session.user_context);
            this.controller_url = action.context.url;
            if (action.context.context) {
                this.given_context = action.context.context;
            }
            this.given_context.active_id = action.context.active_id || action.params.active_id || 1;
            this.given_context.model = action.context.active_model || false;
            this.given_context.ttype = action.context.ttype || false;
            this.given_context.auto_unfold = action.context.auto_unfold || false;
            this.given_context.lot_name = action.context.lot_name || false;
            this.given_context.selected_journal = false;
            this.given_context.selected_exercice = false;
            this.given_context.selected_periode = false;
            return this._super.apply(this, arguments);
        },
        willStart: function() {
            var res_journals = this._rpc({
                model: 'l10n_dz.plan_comptable',
                method: 'get_journals',
                args: []
            }).then(function(results) {
                journals = results;
            });

            var res_exercices = this._rpc({
                model: 'l10n_dz.plan_comptable',
                method: 'get_exercices',
                args: []
            }).then(function(results) {
                exercices = results;
            });

            var res_periodes = this._rpc({
                model: 'l10n_dz.plan_comptable',
                method: 'get_periodes1',
                args: []
            }).then(function(results) {
                periodes = results;
            });

            return Promise.all([this._super.apply(this, arguments), this.get_html()]);
        },
        set_html: function() {
            var self = this;
            var def = Promise.resolve();
            if (!this.report_widget) {
                this.report_widget = new ReportWidget(this, this.given_context);
                def = this.report_widget.appendTo(this.$el);
            }
            return def.then(function() {
                self.report_widget.$el.html(self.html);
                if (self.given_context.auto_unfold) {
                    _.each(self.$el.find('.fa-caret-right'), function(line) {
                        self.report_widget.autounfold(line, self.given_context.lot_name);
                    });
                }
            });
        },
        start: async function() {
            this.controlPanelProps.cp_content = {
                $buttons: this.$buttons,
                $searchview: this.$searchView
            };
            await this._super(...arguments);
            this.set_html();
        },
        // // Fetches the html and is previous report.context if any, else create it
        // get_html: function() {
        //     var self = this;
        //     var defs = [];
        //     return this._rpc({
        //         model: 'l10n_dz.plan_comptable',
        //         method: 'get_html',
        //         args: [self.given_context],
        //     })
        //     .then(function(result) {
        //         self.html = result.html;
        //         self.renderSearch();
        //         defs.push(self.update_cp());
        //         return Promise.all(defs);
        //     });
        // },
        get_html: async function() {
            const { html } = await this._rpc({
                args: [this.given_context],
                method: 'get_html',
                model: 'l10n_dz.plan_comptable',
            });
            this.html = html;
            this.renderSearch();
        },
        // // Updates the control panel and render the elements that have yet to be rendered
        update_cp: function() {
            if (!this.$buttons && !this.searchview) {
                this.renderSearch();
            }
            var status = {
                cp_content: {
                    $buttons: this.$buttons,
                    $searchview: this.$searchView
                },
            };
            return this.updateControlPanel(status);
        },
        // update_cp: function() {
        //     if (!this.$buttons && !this.$searchview) {
        //         this.renderSearch();
        //     }
        //     this.controlPanelProps.cp_content = {
        //         $buttons: this.$buttons,
        //         $searchview: this.$searchView
        //     };
        //     return this.updateControlPanel();
        // },
        renderSearch: function() {
            var self = this;

            this.$buttons = $(QWeb.render("planComptableReports.buttons", {}));
            this.$searchView = $(QWeb.render('eloapps_solde_compte.report_solde_compte_search', {
                'journals': journals,
                'exercices': exercices,
                'periodes': periodes,
                'selected_exercice': self.given_context.selected_exercice,
            }));

            this.$searchView.find('.o_filtrer_journals').on('change', this._onChangeJournal.bind(this));
            this.$searchView.find('.o_filtrer_exercices').on('change', this._onChangeExercice.bind(this));
            this.$searchView.find('.o_filtrer_periodes').on('change', this._onChangePeriode.bind(this));

            return this.$buttons;
        },
        _onChangeJournal: function(ev) {
            var selected_journal = $("option:selected", $(ev.currentTarget)).data('type');
            this.given_context.selected_journal = selected_journal;

            this._reload();
        },
        _onChangeExercice: function(ev) {
            var selected_exercice = $("option:selected", $(ev.currentTarget)).data('type');
            this.given_context.selected_exercice = selected_exercice;
            this.given_context.selected_periode = 0;

            var res_periodes = this._rpc({
                model: 'l10n_dz.plan_comptable',
                method: 'get_periodes1',
                args: [],
            }, { async: false }).then(function(results) {
                periodes = results;
            });

            $("#select_periodes").empty();
            $("#select_periodes").append(new Option("--", 0));
            for (var i = 0; i < periodes.length; i++)
                if (selected_exercice == periodes[i]['exercice_id'])
                    $("#select_periodes").append(new Option(periodes[i]['name'], periodes[i]['id']));

            this._reload();
        },
        _onChangePeriode: function(ev) {
            var selected_periode = parseInt($("option:selected", $(ev.currentTarget))[0].value);
            this.given_context.selected_periode = selected_periode;
            this._reload();
        },
        _reload: function() {
            var self = this;

            return this.get_html().then(function() {
                var selected_journal = self.given_context.selected_journal;

                if (selected_journal)
                    self.$('.o_filtrer_journals').val(selected_journal)
                else if (typeof(selected_journal) == 'number' && selected_journal == 0)
                    self.$('.o_filtrer_journals').val(selected_journal)

                var selected_exercice = self.given_context.selected_exercice;

                if (selected_exercice)
                    self.$('.o_filtrer_exercices').val(selected_exercice)
                else if (typeof(selected_exercice) == 'number' && selected_exercice == 0)
                    self.$('.o_filtrer_exercices').val(selected_exercice)

                var selected_periode = self.given_context.selected_periode;

                if (selected_periode)
                    self.$('.o_filtrer_periodes').val(selected_periode)
                else if (typeof(selected_periode) == 'number' && selected_periode == 0)
                    self.$('.o_filtrer_periodes').val(selected_periode)

                self.set_html();
                self.renderSearch();
            });
        },
        do_show: function() {
            this._super();
            this.update_cp();
        },
    });

    core.action_registry.add("l10n_dz_report_tag", l10n_dz_report_tag);
    return l10n_dz_report_tag;
});