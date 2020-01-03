var _createClass = function () {
    function defineProperties(target, props) {
        for (var i = 0; i < props.length; i++) {
            var descriptor = props[i];
            descriptor.enumerable = descriptor.enumerable || false;
            descriptor.configurable = true;
            if ("value" in descriptor) descriptor.writable = true;
            Object.defineProperty(target, descriptor.key, descriptor);
        }
    }

    return function (Constructor, protoProps, staticProps) {
        if (protoProps) defineProperties(Constructor.prototype, protoProps);
        if (staticProps) defineProperties(Constructor, staticProps);
        return Constructor;
    };
}();

function _classCallCheck(instance, Constructor) {
    if (!(instance instanceof Constructor)) {
        throw new TypeError("Cannot call a class as a function");
    }
}

function _possibleConstructorReturn(self, call) {
    if (!self) {
        throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
    }
    return call && (typeof call === "object" || typeof call === "function") ? call : self;
}

function _inherits(subClass, superClass) {
    if (typeof superClass !== "function" && superClass !== null) {
        throw new TypeError("Super expression must either be null or a function, not " + typeof superClass);
    }
    subClass.prototype = Object.create(superClass && superClass.prototype, {
        constructor: {
            value: subClass,
            enumerable: false,
            writable: true,
            configurable: true
        }
    });
    if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass;
}

/*
 * This file is part of SchoolApps.
 *
 * SchoolApps is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License.
 *
 * SchoolApps is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with SchoolApps.  If not, see <http://www.gnu.org/licenses/>.
 */

/*
 * This file is part of SchoolApps.
 *
 * SchoolApps is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License.
 *
 * SchoolApps is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with SchoolApps.  If not, see <http://www.gnu.org/licenses/>.
 */

var OPTIONS_ONLINE_COMMON = ["Portal ist nicht erreichbar", "Fehlermeldung(en) tauchen auf", "Anmeldung funktioniert nicht", "Zugangsdaten vergessen"];

var BASIC_OPTIONS = [{
    id: "infrastructureIssues",
    name: "Infrastrukturprobleme",
    options: [{
        id: "presentationDeviceIssue",
        name: "Problem mit Beamer/Fernseher",
        helpText: "Bitte wähle aus, wo der Beamer bzw. Fernseher steht!"
    }, {
        id: "printerIssue",
        name: "Problem mit einem Drucker",
        helpText: "Bitte nenne uns in der Beschreibung das Modell des Druckers, damit wir genau wissen, welchen Drucker du meinst!"
    }, {
        id: "subMonitorIssue",
        name: "Vertretungsplanmonitor funktioniert nicht",
        helpText: "Nenne uns bitte in der Beschreibung ggf. weitere Informationen!"
    }, {
        id: "aulaIssue",
        name: "Problem in der Aula (→Technik-AG)",
        helpText: "Deine Anfrage wird direkt an die Technik-AG weitergeleitet."
    }, {
        id: "wlanIssue",
        name: "Probleme mit dem Schul-WLAN (kath-schueler/lehrer)",
        helpText: "Nenne uns bitte unbedingt auch den Ort in der Schule, an dem das Problem auftrat."
    }]
}, {
    id: "onlineIssues",
    name: "Webservices",
    options: [{
        id: "forum",
        name: "Forum (ILIAS)",
        options: OPTIONS_ONLINE_COMMON.concat(["Ich kann meinen Kurs bzw. Klasse nicht sehen/finden.", "Ich kann keine Dateien hochladen.", "Es taucht eine weiße Seite auf.", "Ich habe falsche Informationen gefunden."])
    }, {
        id: "mail",
        name: "Webmail/Mailserver",
        options: OPTIONS_ONLINE_COMMON.concat(["Mein E-Mail-Programm funktioniert mit meiner …@katharineum.de-Adresse nicht.", "Ich bekomme keine E-Mails bzw. kann keine senden."])
    }, {
        id: "schoolapps",
        name: "SchoolApps",
        options: OPTIONS_ONLINE_COMMON.concat(["Der Stundenplan/Vertretungsplan ist falsch.", "Ich bin der falschen Klasse zugeordnet.", "Ich habe einen Fehler gefunden."])
    }, {
        id: "subOrMenu",
        name: "Vertretungsplan/Speiseplan",
        options: OPTIONS_ONLINE_COMMON.concat(["Kein Vertretungsplan zu sehen", "Falscher Vertretungsplan zu sehen", "Kein Speiseplan zu sehen", "Falscher Speiseplan zu sehen"])
    }, {
        id: "website",
        name: "Website (katharineum-zu-luebeck.de)",
        options: ["Website nicht erreichbar", "Falsche Inhalte vorhanden", "Typografiefehler"]

    }, {
        id: "otherOnlineIssue",
        name: "Andere Anwendung"
    }]
}, {
    id: "deviceIssues",
    name: "Probleme am Computer/Notebook",
    options: [{
        id: "loginIssue",
        name: "Anmeldeproblem/Passwort vergessen"
    }, {
        id: "internetIssue",
        name: "Internetproblem"
    }, {
        id: "noReaction",
        name: "Programm-/Computerabsturz (keine Reaktion)"
    }, {
        id: "powerOffNoBoot",
        name: "Computer/Notebook ist ausgegangen/startet nicht"
    }, {
        id: "speedIssue",
        name: "Computer/Notebook zu langsam"
    }, {
        id: "noUSB",
        name: "USB-Stick wird nicht erkannt"
    }, {
        id: "noOpenTray",
        name: "CD/DVD-Laufwerk öffnet sich nicht"
    }, {
        id: "noCDDVD",
        name: "CD/DVD wird nicht erkannt/abgespielt"
    }, {
        id: "keyboardMouse",
        name: "Tastatur/Maus funktioniert nicht"
    }, {
        id: "missingHardware",
        name: "Tastatur/Maus/Lautsprecher/etc. fehlt"
    }, {
        id: "missingKeys",
        name: "Fehlende Tasten auf der Tastatur"
    }, {
        id: "hardwareMisc",
        name: "Andere Hardware defekt / Äußere Schäden"
    }]
}, {
    id: "otherIssues",
    name: "Andere Probleme",
    options: [{
        id: "extra",
        name: "Sonstiges"
    }]
}];

var OTHER_LOCATIONS = ["Notebookwagen 1. Stock/R 2.06", "Notebookwagen 2. Stock/R 2.10", "Notebookwagen 3. Stock/Physik", "Internetcafe", "Infopoint/Sekretariatsvorraum", "Lehrerzimmer (Vorraum)", "Lehrerzimmer (Hauptraum)"];

function getCategoryOfOption(option) {
    var _iteratorNormalCompletion = true;
    var _didIteratorError = false;
    var _iteratorError = undefined;

    try {
        for (var _iterator = BASIC_OPTIONS[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
            var category = _step.value;

            // console.log(category);
            var _iteratorNormalCompletion2 = true;
            var _didIteratorError2 = false;
            var _iteratorError2 = undefined;

            try {
                for (var _iterator2 = category.options[Symbol.iterator](), _step2; !(_iteratorNormalCompletion2 = (_step2 = _iterator2.next()).done); _iteratorNormalCompletion2 = true) {
                    var opt = _step2.value;

                    // console.log(opt);
                    if (opt.id === option) {
                        return category.id;
                    }
                }
            } catch (err) {
                _didIteratorError2 = true;
                _iteratorError2 = err;
            } finally {
                try {
                    if (!_iteratorNormalCompletion2 && _iterator2.return) {
                        _iterator2.return();
                    }
                } finally {
                    if (_didIteratorError2) {
                        throw _iteratorError2;
                    }
                }
            }
        }
    } catch (err) {
        _didIteratorError = true;
        _iteratorError = err;
    } finally {
        try {
            if (!_iteratorNormalCompletion && _iterator.return) {
                _iterator.return();
            }
        } finally {
            if (_didIteratorError) {
                throw _iteratorError;
            }
        }
    }
}

function getOption(option) {
    var _iteratorNormalCompletion3 = true;
    var _didIteratorError3 = false;
    var _iteratorError3 = undefined;

    try {
        for (var _iterator3 = BASIC_OPTIONS[Symbol.iterator](), _step3; !(_iteratorNormalCompletion3 = (_step3 = _iterator3.next()).done); _iteratorNormalCompletion3 = true) {
            var category = _step3.value;
            var _iteratorNormalCompletion4 = true;
            var _didIteratorError4 = false;
            var _iteratorError4 = undefined;

            try {
                for (var _iterator4 = category.options[Symbol.iterator](), _step4; !(_iteratorNormalCompletion4 = (_step4 = _iterator4.next()).done); _iteratorNormalCompletion4 = true) {
                    var opt = _step4.value;

                    if (opt.id === option) {
                        return opt;
                    }
                }
            } catch (err) {
                _didIteratorError4 = true;
                _iteratorError4 = err;
            } finally {
                try {
                    if (!_iteratorNormalCompletion4 && _iterator4.return) {
                        _iterator4.return();
                    }
                } finally {
                    if (_didIteratorError4) {
                        throw _iteratorError4;
                    }
                }
            }
        }
    } catch (err) {
        _didIteratorError3 = true;
        _iteratorError3 = err;
    } finally {
        try {
            if (!_iteratorNormalCompletion3 && _iterator3.return) {
                _iterator3.return();
            }
        } finally {
            if (_didIteratorError3) {
                throw _iteratorError3;
            }
        }
    }
}

var Select = function (_React$Component) {
    _inherits(Select, _React$Component);

    function Select() {
        _classCallCheck(this, Select);

        return _possibleConstructorReturn(this, (Select.__proto__ || Object.getPrototypeOf(Select)).apply(this, arguments));
    }

    _createClass(Select, [{
        key: "render",
        value: function render() {
            return React.createElement(
                "select",
                {onChange: this.props.onChange, defaultValue: "no", required: this.props.show},
                React.createElement(
                    "option",
                    {value: "no", disabled: true},
                    "Nichts ausgew\xE4hlt"
                ),
                this.props.values.map(function (val, i) {
                    return React.createElement(
                        "option",
                        {value: val, key: i},
                        val
                    );
                }),
                React.createElement(
                    "option",
                    {value: "extra"},
                    this.props.defaultValue
                )
            );
        }
    }]);

    return Select;
}(React.Component);

Select.propTypes = {
    onChange: PropTypes.func.isRequired,
    values: PropTypes.array.isRequired,
    defaultValue: PropTypes.string,
    show: PropTypes.bool.isRequired

};

Select.defaultProps = {
    defaultValue: "Sonstiges"
};

var Input = function (_React$Component2) {
    _inherits(Input, _React$Component2);

    function Input() {
        _classCallCheck(this, Input);

        return _possibleConstructorReturn(this, (Input.__proto__ || Object.getPrototypeOf(Input)).apply(this, arguments));
    }

    _createClass(Input, [{
        key: "render",
        value: function render() {
            return React.createElement(
                "div",
                {
                    className: (this.props.show ? "" : "hide ") + "input-field col s12 m12 l4"
                },
                React.createElement(
                    "i",
                    {className: "material-icons prefix"},
                    this.props.icon
                ),
                this.props.children,
                React.createElement(
                    "label",
                    null,
                    this.props.label
                )
            );
        }
    }]);

    return Input;
}(React.Component);

Input.propTypes = {
    icon: PropTypes.string,
    show: PropTypes.bool,
    label: PropTypes.string.isRequired,
    children: PropTypes.object.isRequired
};

Input.defaultProps = {
    icon: "list",
    show: false
};

var REBUSDynSelect = function (_React$Component3) {
    _inherits(REBUSDynSelect, _React$Component3);

    function REBUSDynSelect() {
        _classCallCheck(this, REBUSDynSelect);

        var _this3 = _possibleConstructorReturn(this, (REBUSDynSelect.__proto__ || Object.getPrototypeOf(REBUSDynSelect)).call(this));

        _this3._onCategoryChanges = function (e) {
            var opt = e.target.value;
            var category = getCategoryOfOption(opt);
            var option = getOption(opt);

            // Get matching helper text
            var helpText = option.helpText || _this3.state.helpText;
            if (category === "deviceIssues") {
                helpText = "Wähle bitte das Gerät mit dem Problem aus! Bitte vergiss nicht, uns das Problem unten genauer zu beschreiben!";
            } else if (category === "onlineIssues") {
                helpText = "Bitte konkretisiere das Problem durch eine Auswahl und gib bitte unten genauere Informationen an.";
            } else if (category === "otherIssues") {
                helpText = "Da es sich scheinbar um ein seltenes oder noch nicht erfasstes Problem handelt, gib uns bitte besonders viele Informationen.";
            }

            // Update state
            _this3.setState({
                selectedCategory: category,
                selectedOption: option,
                step: 1,
                helpText: helpText
            });
        };

        _this3._onSetB = function (e) {
            var val = e.target.value;
            _this3.setState({
                valueB: val,
                step: 2
            });
        };

        _this3._onSetC = function (e) {
            var val = e.target.value;
            _this3.setState({
                valueC: val,
                step: 2
            });
        };

        _this3.state = {
            selectedCategory: "noCategory",
            selectedOption: null,
            helpText: "Wähle bitte eine Kategorie aus!",
            valueB: "",
            valueC: "",
            step: 0
        };
        return _this3;
    }

    _createClass(REBUSDynSelect, [{
        key: "componentDidMount",
        value: function componentDidMount() {
            // Init materialize selects
            var elems = document.querySelectorAll('select');
            M.FormSelect.init(elems, {});
        }
    }, {
        key: "render",
        value: function render() {
            var LOCATIONS = this.props.rooms.concat(OTHER_LOCATIONS);
            var LOCATIONS_WITH_POSSIBLE_PRESENTATION_DEVICE = this.props.rooms;
            LOCATIONS.sort();

            // console.log(this.state);
            var that = this;
            var sC = this.state.selectedCategory;
            var sO = this.state.selectedOption ? this.state.selectedOption.id : null;
            var step = this.state.step;
            // console.log(BASIC_OPTIONS[2].options);
            return React.createElement(
                "div",
                {className: "App"},
                React.createElement(
                    "div",
                    {className: "row"},
                    React.createElement(
                        "div",
                        {
                            className: "input-field col s12 m12 l4"
                        },
                        React.createElement(
                            "i",
                            {className: "material-icons prefix"},
                            "list"
                        ),
                        React.createElement(
                            "select",
                            {
                                onChange: this._onCategoryChanges, defaultValue: "noCategory", className: "validate",
                                required: true
                            },
                            "-",
                            React.createElement(
                                "option",
                                {value: "noCategory", disabled: true},
                                "Keine Kategorie ausgew\xE4hlt"
                            ),
                            BASIC_OPTIONS.map(function (category) {
                                return React.createElement(
                                    "optgroup",
                                    {label: category.name, key: category.id},
                                    category.options.map(function (option) {
                                        return React.createElement(
                                            "option",
                                            {value: option.id, key: option.id},
                                            option.name
                                        );
                                    })
                                );
                            })
                        ),
                        React.createElement(
                            "label",
                            null,
                            "Kategorie"
                        )
                    ),
                    React.createElement(
                        Input,
                        {label: "Ort des Computer/Notebook", icon: "location_on", show: sC === "deviceIssues"},
                        React.createElement(Select, {
                            onChange: this._onSetB, values: LOCATIONS, defaultValue: "Anderer Ort",
                            show: sC === "deviceIssues"
                        })
                    ),
                    React.createElement(
                        Input,
                        {
                            label: "Ort des Beamer/Fernseher", icon: "location_on",
                            show: sO === "presentationDeviceIssue"
                        },
                        React.createElement(Select, {
                            onChange: this._onSetB, values: LOCATIONS_WITH_POSSIBLE_PRESENTATION_DEVICE,
                            defaultValue: "Anderer Raum", show: sO === "presentationDeviceIssue"
                        })
                    ),
                    React.createElement(
                        Input,
                        {label: "Art des Problems", icon: "bug_report", show: sO === "printerIssue"},
                        React.createElement(Select, {
                            onChange: this._onSetB,
                            values: ["Papierstau", "Toner leer", "Papier leer", "Drucker bekommt keine Daten"],
                            defaultValue: "Anderes Problem", show: sO === "subMonitorIssue"
                        })
                    ),
                    React.createElement(
                        Input,
                        {label: "Art des Problems", icon: "bug_report", show: sO === "subMonitorIssue"},
                        React.createElement(Select, {
                            onChange: this._onSetB,
                            values: ["Schwarzer Bildschirm", "Tage wechseln nicht (Eingefroren)"],
                            defaultValue: "Anderes Problem", show: sO === "subMonitorIssue"
                        })
                    ),
                    React.createElement(
                        Input,
                        {label: "Art des Problems", icon: "bug_report", show: sO === "wlanIssue"},
                        React.createElement(Select, {
                            onChange: this._onSetB,
                            values: ["Kein Empfang", "Zugangsdaten funktionieren nicht", "Geschwindigkeit zu langsam"],
                            defaultValue: "Anderes Problem", show: sO === "wlanIssue"
                        })
                    ),
                    BASIC_OPTIONS[1].options.map(function (opt) {
                        if (opt.options) {
                            return React.createElement(
                                Input,
                                {
                                    label: "Art des Problems", icon: "bug_report",
                                    show: sC === "onlineIssues" && sO === opt.id, key: opt.id
                                },
                                React.createElement(Select, {
                                    onChange: that._onSetB,
                                    values: opt.options,
                                    defaultValue: "Anderes Problem", show: sC === "onlineIssues" && sO === opt.id,
                                    key: opt.id
                                })
                            );
                        } else {
                            return React.createElement("p", null);
                        }
                    }),
                    React.createElement(
                        Input,
                        {
                            label: "Handelt es sich um einen Beamer oder einen Fernseher?", icon: "tv",
                            show: sO === "presentationDeviceIssue" && step === 2
                        },
                        React.createElement(Select, {
                            onChange: this._onSetC, values: ["Beamer", "Fernseher/Bildschirm"],
                            defaultValue: "Sonstiges", show: sO === "presentationDeviceIssue" && step === 2
                        })
                    ),
                    React.createElement(
                        Input,
                        {
                            label: "Ort des Druckers", icon: "location_on",
                            show: sO === "printerIssue" && step === 2
                        },
                        React.createElement(Select, {
                            onChange: this._onSetC, values: LOCATIONS,
                            defaultValue: "Anderer Raum", show: sO === "presentationDeviceIssue"
                        })
                    ),
                    React.createElement(
                        Input,
                        {
                            label: "Um welches WLAN-Netzwerk handelt es sich?", icon: "wifi",
                            show: sO === "wlanIssue" && step === 2
                        },
                        React.createElement(Select, {
                            onChange: this._onSetC,
                            values: ["kath-schueler", "kath-lehrer", "kath-edu", "kath-gaeste"],
                            defaultValue: "-", show: sO === "wlanIssue" && step === 2
                        })
                    ),
                    React.createElement(
                        "div",
                        {
                            className: (sC === "deviceIssues" && step === 2 ? "" : "hide ") + "input-field col s12 m12 l4"
                        },
                        React.createElement(
                            "i",
                            {className: "material-icons prefix"},
                            "device_unknown"
                        ),
                        React.createElement("input", {
                            type: "text", id: "valc", onChange: this._onSetC,
                            required: sC === "deviceIssues" && step === 2, className: "validate"
                        }),
                        React.createElement(
                            "label",
                            {htmlFor: "valc"},
                            "Um welches Ger\xE4t handelt es sich?"
                        )
                    ),
                    React.createElement(
                        "div",
                        {className: "col s12"},
                        React.createElement(
                            "p",
                            null,
                            React.createElement(
                                "i",
                                {className: "material-icons left"},
                                "info"
                            ),
                            this.state.helpText
                        )
                    )
                ),
                React.createElement(
                    "div",
                    null,
                    React.createElement("input", {
                        type: "hidden", name: "a",
                        value: this.state.selectedOption ? this.state.selectedOption.name : ""
                    }),
                    React.createElement("input", {type: "hidden", name: "b", value: this.state.valueB}),
                    React.createElement("input", {type: "hidden", name: "c", value: this.state.valueC})
                )
            );
        }
    }]);

    return REBUSDynSelect;
}(React.Component);

REBUSDynSelect.propTypes = {
    rooms: PropTypes.array.isRequired
};

$(document).ready(function () {
    var domContainer = document.querySelector('#dynselect');
    ReactDOM.render(React.createElement(REBUSDynSelect, props), domContainer);
});