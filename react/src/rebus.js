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

const OPTIONS_ONLINE_COMMON = [
    "Portal ist nicht erreichbar",
    "Fehlermeldung(en) tauchen auf",
    "Anmeldung funktioniert nicht",
    "Zugangsdaten vergessen"
];

const BASIC_OPTIONS = [
    {
        id: "infrastructureIssues",
        name: "Infrastrukturprobleme",
        options: [
            {
                id: "presentationDeviceIssue",
                name: "Problem mit Beamer/Fernseher",
                helpText: "Bitte wähle aus, wo der Beamer bzw. Fernseher steht!"
            },
            {
                id: "printerIssue",
                name: "Problem mit einem Drucker",
                helpText: "Bitte nenne uns in der Beschreibung das Modell des Druckers, damit wir genau wissen, welchen Drucker du meinst!"
            },
            {
                id: "subMonitorIssue",
                name: "Vertretungsplanmonitor funktioniert nicht",
                helpText: "Nenne uns bitte in der Beschreibung ggf. weitere Informationen!"
            },
            {
                id: "aulaIssue",
                name: "Problem in der Aula (→Technik-AG)",
                helpText: "Deine Anfrage wird direkt an die Technik-AG weitergeleitet."
            },
            {
                id: "wlanIssue",
                name: "Probleme mit dem Schul-WLAN (kath-schueler/lehrer)",
                helpText: "Nenne uns bitte unbedingt auch den Ort in der Schule, an dem das Problem auftrat."
            },
        ]
    },
    {
        id: "onlineIssues",
        name: "Webservices",
        options: [
            {
                id: "forum",
                name: "Forum (ILIAS)",
                options: OPTIONS_ONLINE_COMMON.concat([
                    "Ich kann meinen Kurs bzw. Klasse nicht sehen/finden.",
                    "Ich kann keine Dateien hochladen.",
                    "Es taucht eine weiße Seite auf.",
                    "Ich habe falsche Informationen gefunden.",
                ])
            },
            {
                id: "mail",
                name: "Webmail/Mailserver",
                options: OPTIONS_ONLINE_COMMON.concat([
                    "Mein E-Mail-Programm funktioniert mit meiner …@katharineum.de-Adresse nicht.",
                    "Ich bekomme keine E-Mails bzw. kann keine senden."
                ])
            },
            {
                id: "schoolapps",
                name: "SchoolApps",
                options: OPTIONS_ONLINE_COMMON.concat([
                    "Der Stundenplan/Vertretungsplan ist falsch.",
                    "Ich bin der falschen Klasse zugeordnet.",
                    "Ich habe einen Fehler gefunden."
                ])
            },
            {
                id: "subOrMenu",
                name: "Vertretungsplan/Speiseplan",
                options: OPTIONS_ONLINE_COMMON.concat([
                    "Kein Vertretungsplan zu sehen",
                    "Falscher Vertretungsplan zu sehen",
                    "Kein Speiseplan zu sehen",
                    "Falscher Speiseplan zu sehen"
                ])
            },
            {
                id: "website",
                name: "Website (katharineum-zu-luebeck.de)",
                options: [
                    "Website nicht erreichbar",
                    "Falsche Inhalte vorhanden",
                    "Typografiefehler"
                ]

            },
            {
                id: "otherOnlineIssue",
                name: "Andere Anwendung"
            },
        ]
    },
    {
        id: "deviceIssues",
        name: "Probleme am Computer/Notebook",
        options: [
            {
                id: "loginIssue",
                name: "Anmeldeproblem/Passwort vergessen"
            },
            {
                id: "internetIssue",
                name: "Internetproblem"
            },
            {
                id: "noReaction",
                name: "Programm-/Computerabsturz (keine Reaktion)"
            },
            {
                id: "powerOffNoBoot",
                name: "Computer/Notebook ist ausgegangen/startet nicht"
            },
            {
                id: "speedIssue",
                name: "Computer/Notebook zu langsam"
            },
            {
                id: "noUSB",
                name: "USB-Stick wird nicht erkannt"
            },
            {
                id: "noOpenTray",
                name: "CD/DVD-Laufwerk öffnet sich nicht"
            },
            {
                id: "noCDDVD",
                name: "CD/DVD wird nicht erkannt/abgespielt"
            },
            {
                id: "keyboardMouse",
                name: "Tastatur/Maus funktioniert nicht"
            },
            {
                id: "missingHardware",
                name: "Tastatur/Maus/Lautsprecher/etc. fehlt"
            },
            {
                id: "missingKeys",
                name: "Fehlende Tasten auf der Tastatur"
            },
            {
                id: "hardwareMisc",
                name: "Andere Hardware defekt / Äußere Schäden"
            }


        ]
    },

    {
        id: "otherIssues",
        name: "Andere Probleme",
        options: [
            {
                id: "extra",
                name: "Sonstiges"
            }
        ]
    },
];


const OTHER_LOCATIONS = [
    "Notebookwagen 1. Stock/R 2.06",
    "Notebookwagen 2. Stock/R 2.10",
    "Notebookwagen 3. Stock/Physik",
    "Internetcafe",
    "Infopoint/Sekretariatsvorraum",
    "Lehrerzimmer (Vorraum)",
    "Lehrerzimmer (Hauptraum)"
];


function getCategoryOfOption(option) {
    for (const category of BASIC_OPTIONS) {
        // console.log(category);
        for (const opt of category.options) {
            // console.log(opt);
            if (opt.id === option) {
                return category.id;
            }
        }
    }
}


function getOption(option) {
    for (const category of BASIC_OPTIONS) {
        for (const opt of category.options) {
            if (opt.id === option) {
                return opt;
            }
        }
    }
}

class Select extends React.Component {
    render() {
        return <select onChange={this.props.onChange} defaultValue={"no"} required={this.props.show}>
            <option value={"no"} disabled={true}>Nichts ausgewählt</option>
            {this.props.values.map(function (val, i) {
                return <option value={val} key={i}>{val}</option>;
            })}
            <option value={"extra"}>{this.props.defaultValue}</option>
        </select>
    }
}

Select.propTypes = {
    onChange: PropTypes.func.isRequired,
    values: PropTypes.array.isRequired,
    defaultValue: PropTypes.string,
    show: PropTypes.bool.isRequired

};

Select.defaultProps = {
    defaultValue: "Sonstiges"
};

class Input extends React.Component {
    render() {
        return <div
            className={(this.props.show ? "" : "hide ") + "input-field col s12 m12 l4"
            }>
            <i className={"material-icons prefix"}>{this.props.icon}</i>
            {this.props.children}
            <label>{this.props.label}</label>
        </div>;
    }
}

Input.propTypes = {
    icon: PropTypes.string,
    show: PropTypes.bool,
    label: PropTypes.string.isRequired,
    children: PropTypes.object.isRequired
};

Input.defaultProps = {
    icon: "list",
    show: false,
};

class REBUSDynSelect extends React.Component {
    constructor() {
        super();
        this.state = {
            selectedCategory: "noCategory",
            selectedOption: null,
            helpText: "Wähle bitte eine Kategorie aus!",
            valueB: "",
            valueC: "",
            step: 0
        }
    }

    componentDidMount() {
        // Init materialize selects
        const elems = document.querySelectorAll('select');
        M.FormSelect.init(elems, {});
    }

    _onCategoryChanges = (e) => {
        const opt = e.target.value;
        const category = getCategoryOfOption(opt);
        const option = getOption(opt);

        // Get matching helper text
        let helpText = option.helpText || this.state.helpText;
        if (category === "deviceIssues") {
            helpText = "Wähle bitte das Gerät mit dem Problem aus! Bitte vergiss nicht, uns das Problem unten genauer zu beschreiben!"
        } else if (category === "onlineIssues") {
            helpText = "Bitte konkretisiere das Problem durch eine Auswahl und gib bitte unten genauere Informationen an."
        } else if (category === "otherIssues") {
            helpText = "Da es sich scheinbar um ein seltenes oder noch nicht erfasstes Problem handelt, gib uns bitte besonders viele Informationen."
        }

        // Update state
        this.setState({
            selectedCategory: category,
            selectedOption: option,
            step: 1,
            helpText: helpText
        })
    };

    _onSetB = (e) => {
        const val = e.target.value;
        this.setState({
            valueB: val,
            step: 2
        })
    };

    _onSetC = (e) => {
        const val = e.target.value;
        this.setState({
            valueC: val,
            step: 2
        })
    };

    render() {
        let LOCATIONS = this.props.rooms.concat(OTHER_LOCATIONS);
        let LOCATIONS_WITH_POSSIBLE_PRESENTATION_DEVICE = this.props.rooms;
        LOCATIONS.sort();

        // console.log(this.state);
        const that = this;
        const sC = this.state.selectedCategory;
        const sO = this.state.selectedOption ? this.state.selectedOption.id : null;
        const step = this.state.step;
        // console.log(BASIC_OPTIONS[2].options);
        return (
            <div className="App">
                <div className={"row"}>
                    < div
                        className="input-field col s12 m12 l4">
                        <i className={"material-icons prefix"}>list</i>
                        <select onChange={this._onCategoryChanges} defaultValue={"noCategory"} className={"validate"}
                                required={true}>-
                            <option value={"noCategory"} disabled={true}>Keine Kategorie ausgewählt</option>
                            {BASIC_OPTIONS.map(function (category) {
                                return <optgroup label={category.name} key={category.id}>
                                    {category.options.map(function (option) {
                                        return <option value={option.id} key={option.id}>{option.name}</option>;
                                    })}
                                </optgroup>;
                            })}
                            {/*<option value={"extra"}>Sonstiges</option>*/}
                        </select>
                        <label>Kategorie</label>
                    </div>

                    {/* Section B – Device Issues*/}
                    <Input label={"Ort des Computer/Notebook"} icon={"location_on"} show={sC === "deviceIssues"}>
                        <Select onChange={this._onSetB} values={LOCATIONS} defaultValue={"Anderer Ort"}
                                show={sC === "deviceIssues"}/>
                    </Input>

                    {/* Section B – Presentation Device Issues */}
                    <Input label={"Ort des Beamer/Fernseher"} icon={"location_on"}
                           show={sO === "presentationDeviceIssue"}>
                        <Select onChange={this._onSetB} values={LOCATIONS_WITH_POSSIBLE_PRESENTATION_DEVICE}
                                defaultValue={"Anderer Raum"} show={sO === "presentationDeviceIssue"}/>
                    </Input>

                    {/* Section B – Printer Issue */}
                    <Input label={"Art des Problems"} icon={"bug_report"} show={sO === "printerIssue"}>
                        <Select onChange={this._onSetB}
                                values={["Papierstau", "Toner leer", "Papier leer", "Drucker bekommt keine Daten"]}
                                defaultValue={"Anderes Problem"} show={sO === "printerIssue"}/>
                    </Input>

                    {/* Section B – Substitution Monitor Issue */}
                    <Input label={"Art des Problems"} icon={"bug_report"} show={sO === "subMonitorIssue"}>
                        <Select onChange={this._onSetB}
                                values={["Schwarzer Bildschirm", "Tage wechseln nicht (Eingefroren)"]}
                                defaultValue={"Anderes Problem"} show={sO === "subMonitorIssue"}/>
                    </Input>

                    {/* Section B – WLAN Issue */}
                    <Input label={"Art des Problems"} icon={"bug_report"} show={sO === "wlanIssue"}>
                        <Select onChange={this._onSetB}
                                values={["Kein Empfang", "Zugangsdaten funktionieren nicht", "Geschwindigkeit zu langsam"]}
                                defaultValue={"Anderes Problem"} show={sO === "wlanIssue"}/>
                    </Input>

                    {/* Section B – Online Issue*/}
                    {BASIC_OPTIONS[1].options.map(function (opt) {
                        if (opt.options) {
                            return <Input label={"Art des Problems"} icon={"bug_report"}
                                          show={sC === "onlineIssues" && sO === opt.id} key={opt.id}>
                                <Select onChange={that._onSetB}
                                        values={opt.options}
                                        defaultValue={"Anderes Problem"} show={sC === "onlineIssues" && sO === opt.id}
                                        key={opt.id}/>
                            </Input>;
                        } else {
                            return <p/>;
                        }
                    })}


                    {/* Section C – Presentation Device Issues */}
                    <Input label={"Handelt es sich um einen Beamer oder einen Fernseher?"} icon={"tv"}
                           show={sO === "presentationDeviceIssue" && step === 2}>
                        <Select onChange={this._onSetC} values={["Beamer", "Fernseher/Bildschirm"]}
                                defaultValue={"Sonstiges"} show={sO === "presentationDeviceIssue" && step === 2}/>
                    </Input>

                    {/* Section C – Presentation Device Issues */}
                    <Input label={"Ort des Druckers"} icon={"location_on"}
                           show={sO === "printerIssue" && step === 2}>
                        <Select onChange={this._onSetC} values={LOCATIONS}
                                defaultValue={"Anderer Raum"} show={sO === "printerIssue"}/>
                    </Input>

                    {/* Section C – WLAN Issue */}
                    <Input label={"Um welches WLAN-Netzwerk handelt es sich?"} icon={"wifi"}
                           show={sO === "wlanIssue" && step === 2}>
                        <Select onChange={this._onSetC}
                                values={["kath-schueler", "kath-lehrer", "kath-edu", "kath-gaeste"]}
                                defaultValue={"-"} show={sO === "wlanIssue" && step === 2}/>
                    </Input>

                    {/* Section C – Device Issue */}
                    <div
                        className={(sC === "deviceIssues" && step === 2 ? "" : "hide ") + "input-field col s12 m12 l4"
                        }>
                        <i className={"material-icons prefix"}>device_unknown</i>
                        <input type={"text"} id={"valc"} onChange={this._onSetC}
                               required={sC === "deviceIssues" && step === 2} className={"validate"}/>
                        <label htmlFor="valc">Um welches Gerät handelt es sich?</label>
                    </div>

                    {/* Helper Text */}
                    <div className={"col s12"}>
                        <p>
                            <i className={"material-icons left"}>info</i>
                            {this.state.helpText}
                        </p>
                    </div>


                </div>

                {/* Prepare values for Django */}
                <div>
                    <input type={"hidden"} name={"a"}
                           value={this.state.selectedOption ? this.state.selectedOption.name : ""}/>
                    <input type={"hidden"} name={"b"} value={this.state.valueB}/>
                    <input type={"hidden"} name={"c"} value={this.state.valueC}/>
                </div>

            </div>
        );
    }
}

REBUSDynSelect.propTypes = {
    rooms: PropTypes.array.isRequired
};

$(document).ready(function () {
    const domContainer = document.querySelector('#dynselect');
    ReactDOM.render(<REBUSDynSelect {...props}/>, domContainer);
});