"use strict";

var _interopRequireWildcard = require("/home/wethjo/dev/school-apps/dynselect/node_modules/@babel/runtime/helpers/interopRequireWildcard");

var _interopRequireDefault = require("/home/wethjo/dev/school-apps/dynselect/node_modules/@babel/runtime/helpers/interopRequireDefault");

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _classCallCheck2 = _interopRequireDefault(require("/home/wethjo/dev/school-apps/dynselect/node_modules/@babel/runtime/helpers/esm/classCallCheck"));

var _createClass2 = _interopRequireDefault(require("/home/wethjo/dev/school-apps/dynselect/node_modules/@babel/runtime/helpers/esm/createClass"));

var _possibleConstructorReturn2 = _interopRequireDefault(require("/home/wethjo/dev/school-apps/dynselect/node_modules/@babel/runtime/helpers/esm/possibleConstructorReturn"));

var _getPrototypeOf2 = _interopRequireDefault(require("/home/wethjo/dev/school-apps/dynselect/node_modules/@babel/runtime/helpers/esm/getPrototypeOf"));

var _inherits2 = _interopRequireDefault(require("/home/wethjo/dev/school-apps/dynselect/node_modules/@babel/runtime/helpers/esm/inherits"));

var _react = _interopRequireWildcard(require("react"));

require("materialize-css/dist/css/materialize.css");

var _materialize2 = _interopRequireDefault(require("materialize-css/dist/js/materialize"));

var OPTIONS_ONLINE_COMMON = ["Portal ist nicht erreichbar", "Fehlermeldung(en) tauchen auf", "Anmeldung funktiontiert nicht", "Zugangsdaten vergessen"];
var BASIC_OPTIONS = [{
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
  }]
}, {
  id: "infrastructureIssues",
  name: "Infrastrukturprobleme",
  options: [{
    id: "presentationDeviceIssue",
    name: "Problem mit Beamer/Fernseher",
    helpText: "Bitte wähle aus, wo der Beamer bzw. Fernseher steht!"
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
  id: "otherIssues",
  name: "Andere Probleme",
  options: [{
    id: "extra",
    name: "Sonstiges"
  }]
}];
var ROOMS_WITH_PRESENTATION_DEVICE = ["R 0.04", "R 0.05", "R 0.07", "R 0.08"];
var OTHER_LOCATIONS = ["Notebookwagen 1", "NotebookqAFWN 1"];
var LOCATIONS = ROOMS_WITH_PRESENTATION_DEVICE.concat(OTHER_LOCATIONS);

function getCategoryOfOption(option) {
  for (var _i = 0; _i < BASIC_OPTIONS.length; _i++) {
    var category = BASIC_OPTIONS[_i];
    // console.log(category);
    var _iteratorNormalCompletion = true;
    var _didIteratorError = false;
    var _iteratorError = undefined;

    try {
      for (var _iterator = category.options[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
        var opt = _step.value;

        // console.log(opt);
        if (opt.id === option) {
          return category.id;
        }
      }
    } catch (err) {
      _didIteratorError = true;
      _iteratorError = err;
    } finally {
      try {
        if (!_iteratorNormalCompletion && _iterator.return != null) {
          _iterator.return();
        }
      } finally {
        if (_didIteratorError) {
          throw _iteratorError;
        }
      }
    }
  }
}

function getOption(option) {
  for (var _i2 = 0; _i2 < BASIC_OPTIONS.length; _i2++) {
    var category = BASIC_OPTIONS[_i2];
    // console.log(category);
    var _iteratorNormalCompletion2 = true;
    var _didIteratorError2 = false;
    var _iteratorError2 = undefined;

    try {
      for (var _iterator2 = category.options[Symbol.iterator](), _step2; !(_iteratorNormalCompletion2 = (_step2 = _iterator2.next()).done); _iteratorNormalCompletion2 = true) {
        var opt = _step2.value;

        // console.log(opt);
        if (opt.id === option) {
          return opt;
        }
      }
    } catch (err) {
      _didIteratorError2 = true;
      _iteratorError2 = err;
    } finally {
      try {
        if (!_iteratorNormalCompletion2 && _iterator2.return != null) {
          _iterator2.return();
        }
      } finally {
        if (_didIteratorError2) {
          throw _iteratorError2;
        }
      }
    }
  }
}

var Select =
/*#__PURE__*/
function (_Component) {
  (0, _inherits2.default)(Select, _Component);

  function Select() {
    (0, _classCallCheck2.default)(this, Select);
    return (0, _possibleConstructorReturn2.default)(this, (0, _getPrototypeOf2.default)(Select).apply(this, arguments));
  }

  (0, _createClass2.default)(Select, [{
    key: "render",
    value: function render() {
      return _react.default.createElement("select", {
        onChange: this.props.onChange,
        defaultValue: "no",
        required: true
      }, _react.default.createElement("option", {
        value: "no",
        disabled: true
      }, "Nichts ausgew\xE4hlt"), this.props.values.map(function (val, i) {
        return _react.default.createElement("option", {
          value: val,
          key: i
        }, val);
      }), _react.default.createElement("option", {
        value: "extra"
      }, this.props.defaultValue));
    }
  }]);
  return Select;
}(_react.Component);

Select.defaultProps = {
  defaultValue: "Sonstiges"
};

var Input =
/*#__PURE__*/
function (_Component2) {
  (0, _inherits2.default)(Input, _Component2);

  function Input() {
    (0, _classCallCheck2.default)(this, Input);
    return (0, _possibleConstructorReturn2.default)(this, (0, _getPrototypeOf2.default)(Input).apply(this, arguments));
  }

  (0, _createClass2.default)(Input, [{
    key: "render",
    value: function render() {
      return _react.default.createElement("div", {
        className: (this.props.show ? "" : "hide ") + "input-field col s4"
      }, _react.default.createElement("i", {
        className: "material-icons prefix"
      }, this.props.icon), this.props.children, _react.default.createElement("label", null, this.props.label));
    }
  }]);
  return Input;
}(_react.Component);

Input.defaultProps = {
  icon: "list",
  show: false
};

var App =
/*#__PURE__*/
function (_Component3) {
  (0, _inherits2.default)(App, _Component3);

  function App() {
    var _this;

    (0, _classCallCheck2.default)(this, App);
    _this = (0, _possibleConstructorReturn2.default)(this, (0, _getPrototypeOf2.default)(App).call(this));

    _this._onCategoryChanges = function (e) {
      var opt = e.target.value;
      var category = getCategoryOfOption(opt);
      var option = getOption(opt); // Get matching helper text

      var helpText = option.helpText || _this.state.helpText;

      if (category === "deviceIssues") {
        helpText = "Wähle bitte das Gerät mit dem Problem aus! Bitte vergiss nicht, uns das Problem unten genauer zu beschreiben!";
      } else if (category === "onlineIssues") {
        helpText = "Bitte konkretisiere das Problem durch eine Auswahl und gib bitte unten genauere Informationen an.";
      } else if (category === "otherIssues") {
        helpText = "Da es sich scheinbar um ein seltenes oder noch nicht erfasstes Problem handelt, gib uns bitte besonders viele Informationen.";
      } // Update state


      _this.setState({
        selectedCategory: category,
        selectedOption: option,
        step: 1,
        helpText: helpText
      });
    };

    _this._onSetB = function (e) {
      var val = e.target.value;

      _this.setState({
        valueB: val,
        step: 2
      });
    };

    _this._onSetC = function (e) {
      var val = e.target.value;

      _this.setState({
        valueC: val,
        step: 2
      });
    };

    _this.state = {
      selectedCategory: "noCategory",
      selectedOption: null,
      helpText: "Wähle bitte eine Kategorie aus!",
      valueB: "",
      valueC: "",
      step: 0
    };
    return _this;
  }

  (0, _createClass2.default)(App, [{
    key: "componentDidMount",
    value: function componentDidMount() {
      // Init materialize selects
      var elems = document.querySelectorAll('select');

      _materialize2.default.FormSelect.init(elems, {});
    }
  }, {
    key: "render",
    value: function render() {
      console.log(this.state);
      var that = this;
      var sC = this.state.selectedCategory;
      var sO = this.state.selectedOption ? this.state.selectedOption.id : null;
      var step = this.state.step;
      console.log(BASIC_OPTIONS[2].options);
      return _react.default.createElement("div", {
        className: "App"
      }, _react.default.createElement("div", {
        className: "row"
      }, _react.default.createElement("div", {
        className: "input-field col s4"
      }, _react.default.createElement("i", {
        className: "material-icons prefix"
      }, "list"), _react.default.createElement("select", {
        onChange: this._onCategoryChanges,
        defaultValue: "noCategory"
      }, _react.default.createElement("option", {
        value: "noCategory",
        disabled: true
      }, "Keine Kategorie ausgew\xE4hlt"), BASIC_OPTIONS.map(function (category) {
        return _react.default.createElement("optgroup", {
          label: category.name,
          key: category.id
        }, category.options.map(function (option) {
          return _react.default.createElement("option", {
            value: option.id,
            key: option.id
          }, option.name);
        }));
      })), _react.default.createElement("label", null, "Kategorie")), _react.default.createElement(Input, {
        label: "Ort des Computer/Notebook",
        icon: "location_on",
        show: sC === "deviceIssues"
      }, _react.default.createElement(Select, {
        onChange: this._onSetB,
        values: LOCATIONS,
        defaultValue: "Anderer Ort"
      })), _react.default.createElement(Input, {
        label: "Ort des Beamer/Fernseher",
        icon: "location_on",
        show: sO === "presentationDeviceIssue"
      }, _react.default.createElement(Select, {
        onChange: this._onSetB,
        values: ROOMS_WITH_PRESENTATION_DEVICE,
        defaultValue: "Anderer Raum"
      })), _react.default.createElement(Input, {
        label: "Art des Problems",
        icon: "bug_report",
        show: sO === "subMonitorIssue"
      }, _react.default.createElement(Select, {
        onChange: this._onSetB,
        values: ["Schwarzer Bildschirm", "Tage wechseln nicht (Eingefroren)"],
        defaultValue: "Anderer Raum"
      })), _react.default.createElement(Input, {
        label: "Art des Problems",
        icon: "bug_report",
        show: sO === "wlanIssue"
      }, _react.default.createElement(Select, {
        onChange: this._onSetB,
        values: ["Kein Empfang", "Zugangsdaten funktionieren nicht", "Geschwindigkeit zu langsam"],
        defaultValue: "Anderes Problem"
      })), BASIC_OPTIONS[2].options.map(function (opt) {
        if (opt.options) {
          return _react.default.createElement(Input, {
            label: "Art des Problems",
            icon: "bug_report",
            show: sC === "onlineIssues" && sO === opt.id,
            key: opt.id
          }, _react.default.createElement(Select, {
            onChange: that._onSetB,
            values: opt.options,
            defaultValue: "Anderes Problem"
          }));
        } else {
          return _react.default.createElement("p", null);
        }
      }), _react.default.createElement(Input, {
        label: "Handelt es sich um einen Beamer oder einen Fernseher?",
        icon: "tv",
        show: sO === "presentationDeviceIssue" && step === 2
      }, _react.default.createElement(Select, {
        onChange: this._onSetC,
        values: ["Beamer", "Fernseher/Bildschirm"],
        defaultValue: "Sonstiges"
      })), _react.default.createElement(Input, {
        label: "Um welches WLAN-Netzwerk handelt es sich?",
        icon: "wifi",
        show: sO === "wlanIssue" && step === 2
      }, _react.default.createElement(Select, {
        onChange: this._onSetC,
        values: ["kath-schueler", "kath-lehrer", "kath-edu", "kath-gaeste"],
        defaultValue: "-"
      })), _react.default.createElement("div", {
        className: (sC === "deviceIssues" && step === 2 ? "" : "hide ") + "input-field col s4"
      }, _react.default.createElement("i", {
        className: "material-icons prefix"
      }, "device_unknown"), _react.default.createElement("input", {
        type: "text",
        id: "valc",
        onChange: this._onSetC,
        required: true
      }), _react.default.createElement("label", {
        htmlFor: "valc"
      }, "Um welches Ger\xE4t handelt es sich?")), _react.default.createElement("div", {
        className: "col s12"
      }, _react.default.createElement("p", null, _react.default.createElement("i", {
        className: "material-icons left"
      }, "info"), this.state.helpText))), _react.default.createElement("div", null, _react.default.createElement("input", {
        type: "hidden",
        name: "a",
        value: this.state.selectedOption ? this.state.selectedOption.name : ""
      }), _react.default.createElement("input", {
        type: "hidden",
        name: "b",
        value: this.state.valueB
      }), _react.default.createElement("input", {
        type: "hidden",
        name: "c",
        value: this.state.valueC
      })));
    }
  }]);
  return App;
}(_react.Component);

var _default = App;
exports.default = _default;