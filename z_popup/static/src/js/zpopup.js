/** @odoo-module */

import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { _lt } from "@web/core/l10n/translation";
import { CharField } from "@web/views/fields/char/char_field";
import { SelectCreateDialog } from "@web/views/view_dialogs/select_create_dialog";
import { useOwnedDialogs, useService } from "@web/core/utils/hooks";

var rpc = require('web.rpc');

export class PopupWidget extends CharField {
    setup() {
        super.setup();
        this.addDialog = useOwnedDialogs();
    }

    _onInputChange(ev) {
        const newValue = ev.target.value;
        console.log(newValue)
        console.log(this.props.step)
        console.log(this.props.value)
        this._doStep(newValue)
    }

    // create own rpc to get dynamic model and method calling controller
    async _callModelMethod(modelName, methodName, args) {
        var result = await rpc.query({
            route: '/my_rpc',
            params: {
                model_name: modelName,
                method_name: methodName,
                // args: args.length === 0 ? [] : args,
                args: args || [],
            },
        });
        return result;
    }

    // select record on widget
    _onSelectedRecord(records) {
        if (records.length > 0) {
            const selectedRecord = records[0];
            console.log('Selected id', selectedRecord);
            const modelName = this.props.relatedmodel
            const methodName = this.props.relatedaction
            const args = [selectedRecord]

            this._callModelMethod(modelName, methodName, args)
                .then((result) => {
                    console.log('RPC Result:', result); // Log the result to see what it contains
                    console.log('result.name', result.name)
                    if(this.props.value !== result.name){
                        this._doStep(result.name)
                    }
                })
                .catch(function (error) {
                    console.log(error);
                })
        }
    }

    // button action
    _OnCopyClick(ev) {
        console.log(this)
        console.log(this.props.value)
        const my_dialog = this.addDialog(SelectCreateDialog, {
            title: "SELECT",
            noCreate: true,
            multiSelect: true,
            resModel: this.props.relatedmodel,
            context: {},
            domain: [],
            searchViewId: false,
            onSelected: this._onSelectedRecord.bind(this),
            dynamicFilters: [],
        });
    }

    // update values
    _doStep(result) {
        let cval = result
        cval += this.props.step;
        this.updateField(cval);
        this.props.setDirty(this._isSetDirty(cval));
    }

    // resolve props
    updateField(val) {
        return Promise.resolve(this.props.update(val));
    }

    _isSetDirty(val) {
        return this.props.value != val;
    }
}

// set template
PopupWidget.template = "my_popup_widget_template";

// set props/key
PopupWidget.props = {
    ...standardFieldProps,
    name: { type: String, optional: true },
    inputType: { type: String, optional: true },
    placeholder: { type: String, optional: true },
    relatedmodel: { type: String, optional: true },
    relatedaction: { type: String, optional: true },
    step: { type: String, optional: true },
};

// set attrs in widget as options
PopupWidget.displayName = _lt("Numeric Step");
PopupWidget.defaultProps = {
    inputType: "text",
};
PopupWidget.extractProps = ({ attrs }) => {
    return {
        name: attrs.name,
        inputType: attrs.options.type,
        placeholder: attrs.options.placeholder,
        relatedmodel: attrs.relatedModel,
        relatedaction: attrs.relatedAction,
        step: attrs.step || '',  //give default value to seval
    };
};

registry.category("fields").add("popup_widget", PopupWidget);
