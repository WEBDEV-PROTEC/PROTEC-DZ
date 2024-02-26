/** @odoo-module **/
import { browser } from '@web/core/browser/browser';
import { useComponentToModel } from '@mail/component_hooks/use_component_to_model';
import { useService } from "@web/core/utils/hooks";
import { registerMessagingComponent } from '@mail/utils/messaging_component';

const { Component } = owl;

export class PrintnodeStatusMenu extends Component {
    /**
    * @override
    */
    async setup() {
        super.setup();

        this.user = useService("user");

        useComponentToModel({ fieldName: 'component' });
    }

    get printnodeStatusMenu() {
        return this.props.record;
    }
}

Object.assign(PrintnodeStatusMenu, {
    props: { record: Object },
    template: 'printnode_base.StatusMenu',
});

registerMessagingComponent(PrintnodeStatusMenu);
