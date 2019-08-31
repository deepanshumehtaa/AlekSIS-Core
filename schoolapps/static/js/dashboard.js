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

var REFRESH_TIME = 15;

function WithCheckCircleIcon(props) {
    return React.createElement(
        "div",
        {className: "col s12"},
        React.createElement(
            "i",
            {className: "material-icons left green-text"},
            "check_circle"
        ),
        props.children
    );
}

var Dashboard = function (_React$Component) {
    _inherits(Dashboard, _React$Component);

    function Dashboard() {
        _classCallCheck(this, Dashboard);

        var _this = _possibleConstructorReturn(this, (Dashboard.__proto__ || Object.getPrototypeOf(Dashboard)).call(this));

        _this.updateRefreshTime = function () {
            if (_this.state.refreshIn >= 1) {
                if (_this.state.timeout) {
                    window.clearTimeout(_this.state.timeout);
                }
                var timeout = window.setTimeout(_this.updateRefreshTime, 1000);
                _this.setState({refreshIn: _this.state.refreshIn - 1, timeout: timeout});
                console.log("WOrk");
            } else {
                _this.updateData();
            }
        };

        _this.updateData = function () {
            var that = _this;
            $.getJSON(API_URL, function (data) {
                console.log(data);
                if (data) {
                    that.setState(Object.assign({}, data, {refreshIn: REFRESH_TIME + 1}));
                    that.updateRefreshTime();
                }
            });
        };

        _this.state = {
            refreshIn: REFRESH_TIME
        };
        return _this;
    }

    _createClass(Dashboard, [{
        key: "componentDidMount",
        value: function componentDidMount() {
            console.log(API_URL);
            this.updateData();
        }
    }, {
        key: "closeNotification",
        value: function closeNotification(notification) {
        }
    }, {
        key: "render",
        value: function render() {
            return React.createElement(
                "div",
                null,
                React.createElement(
                    "button",
                    {className: "btn-flat right grey-text", onClick: this.updateData},
                    React.createElement(
                        "i",
                        {className: "material-icons left"},
                        "refresh"
                    ),
                    "in ",
                    this.state.refreshIn,
                    " s"
                ),
                React.createElement(
                    "p",
                    {className: "flow-text"},
                    "Willkommen bei SchoolApps!"
                ),
                React.createElement(
                    "div",
                    {className: "alert primary"},
                    React.createElement(
                        "div",
                        null,
                        React.createElement(
                            "i",
                            {className: "material-icons left"},
                            "info"
                        ),
                        React.createElement(
                            "button",
                            {className: "btn-flat right"},
                            React.createElement(
                                "i",
                                {className: "material-icons center"},
                                "close"
                            )
                        ),
                        React.createElement(
                            "strong",
                            null,
                            "Ihr Antrag auf Unterrichtsbefreiung wurde genehmigt"
                        ),
                        React.createElement(
                            "p",
                            null,
                            "Ihr Antrag auf Unterrichtsbefreiung vom 20. August 2019, 08:45 Uhr bis 29. August 2019, 13:10 Uhr wurde von der Schulleitung genehmigt. "
                        )
                    )
                ),
                React.createElement(
                    "div",
                    {className: "row"},
                    React.createElement(
                        "div",
                        {className: "col s12 m8"},
                        React.createElement(
                            "div",
                            {className: "col s12 m6"},
                            React.createElement(
                                "div",
                                {className: "card"},
                                React.createElement(
                                    "div",
                                    {className: "card-content"},
                                    React.createElement(
                                        "span",
                                        {className: "card-title"},
                                        "Vertretungen der ",
                                        React.createElement(
                                            "em",
                                            null,
                                            "Eb"
                                        ),
                                        " f\xFCr heute"
                                    ),
                                    React.createElement(
                                        "p",
                                        null,
                                        "I am a very simple card. I am good at containing small bits of information. I am convenient because I require little markup to use effectively."
                                    )
                                ),
                                React.createElement(
                                    "div",
                                    {className: "card-action"},
                                    React.createElement(
                                        "a",
                                        {href: "#"},
                                        React.createElement(
                                            "span",
                                            {className: "badge new primary-color card-action-badge"},
                                            "SMART PLAN"
                                        ),
                                        "anzeigen"
                                    )
                                )
                            )
                        ),
                        React.createElement(
                            "div",
                            {className: "col s12 m6"},
                            React.createElement(
                                "div",
                                {className: "card"},
                                React.createElement(
                                    "div",
                                    {className: "card-content"},
                                    React.createElement(
                                        "span",
                                        {className: "card-title"},
                                        "Aktuelle Termine"
                                    ),
                                    React.createElement(
                                        "div",
                                        {className: "card-panel event-card"},
                                        React.createElement(
                                            "span",
                                            {className: "title"},
                                            "Sextanereinschulung"
                                        ),
                                        React.createElement("br", null),
                                        "28.Aug. 2019 18:30 - 22:00"
                                    ),
                                    React.createElement(
                                        "div",
                                        {className: "card-panel event-card"},
                                        React.createElement(
                                            "span",
                                            {className: "title"},
                                            "Sextanereinschulung"
                                        ),
                                        React.createElement("br", null),
                                        "28.Aug. 2019 18:30 - 22:00"
                                    )
                                ),
                                React.createElement(
                                    "div",
                                    {className: "card-action"},
                                    React.createElement(
                                        "a",
                                        {href: "https://katharineum-zu-luebeck.de/aktuelles/termine/"},
                                        "Weitere Termine"
                                    )
                                )
                            )
                        ),
                        React.createElement(
                            "div",
                            {className: "col s12 m6"},
                            React.createElement(
                                "div",
                                {className: "card"},
                                React.createElement(
                                    "div",
                                    {className: "card-content"},
                                    React.createElement(
                                        "span",
                                        {className: "card-title"},
                                        "Mein Status"
                                    ),
                                    React.createElement(
                                        "div",
                                        {className: "row"},
                                        React.createElement(
                                            WithCheckCircleIcon,
                                            null,
                                            this.state.user_type_formatted
                                        ),
                                        this.state.user_type === 1 || this.state.user_type === 2 ? React.createElement(
                                            WithCheckCircleIcon,
                                            null,
                                            "Meine Klassen: ",
                                            this.state.classes.join(", ")
                                        ) : "",
                                        this.state.user_type === 1 || this.state.user_type === 2 ? React.createElement(
                                            WithCheckCircleIcon,
                                            null,
                                            "Meine Kurse: ",
                                            this.state.courses.join(", ")
                                        ) : "",
                                        this.state.user_type === 1 ? React.createElement(
                                            WithCheckCircleIcon,
                                            null,
                                            "Meine F\xE4cher: ",
                                            this.state.subjects.join(", ")
                                        ) : "",
                                        this.state.user_type === 1 || this.state.has_wifi ? React.createElement(
                                            WithCheckCircleIcon,
                                            null,
                                            "WLAN"
                                        ) : React.createElement(
                                            "div",
                                            {className: "col"},
                                            React.createElement(
                                                "i",
                                                {className: "material-icons left red-text"},
                                                "cancel"
                                            ),
                                            "Kein WLAN"
                                        )
                                    )
                                )
                            )
                        ),
                        React.createElement(
                            "div",
                            {className: "col s12 m6"},
                            React.createElement(
                                "div",
                                {className: "card"},
                                React.createElement(
                                    "div",
                                    {className: "card-content"},
                                    React.createElement(
                                        "span",
                                        {className: "card-title"},
                                        "Klausuren der ",
                                        React.createElement(
                                            "em",
                                            null,
                                            "Eb"
                                        )
                                    ),
                                    React.createElement(
                                        "div",
                                        {className: "card-panel event-card"},
                                        React.createElement(
                                            "span",
                                            {className: "title"},
                                            "Sextanereinschulung"
                                        ),
                                        React.createElement("br", null),
                                        "28.Aug. 2019 18:30 - 22:00"
                                    ),
                                    React.createElement(
                                        "div",
                                        {className: "card-panel event-card"},
                                        React.createElement(
                                            "span",
                                            {className: "title"},
                                            "Sextanereinschulung"
                                        ),
                                        React.createElement("br", null),
                                        "28.Aug. 2019 18:30 - 22:00"
                                    )
                                ),
                                React.createElement(
                                    "div",
                                    {className: "card-action"},
                                    React.createElement(
                                        "a",
                                        {href: "https://katharineum-zu-luebeck.de/aktuelles/termine/"},
                                        "Alle Klausuren"
                                    )
                                )
                            )
                        )
                    ),
                    React.createElement(
                        "div",
                        {className: "col s12 m4"},
                        React.createElement(
                            "div",
                            {className: "card"},
                            React.createElement(
                                "div",
                                {className: "card-image"},
                                React.createElement("img", {
                                    src: "https://katharineum-zu-luebeck.de/wp-content/uploads/2019/08/E969562D-C413-4B18-AC63-26C768499BFF.jpeg"
                                }),
                                React.createElement(
                                    "span",
                                    {className: "card-title"},
                                    "Ein gro\xDFer Tag - Die Einschulung der neuen Sextaner"
                                )
                            ),
                            React.createElement(
                                "div",
                                {className: "card-content"},
                                React.createElement(
                                    "p",
                                    null,
                                    "Am 13.08. war es wieder so weit: am Katharineum wurden die neuen Sextaner willkommen gehei\xDFen. Bereits zehn Minuten vor Beginn der allj\xE4hrlichen Veranstaltung war die\u2026"
                                )
                            ),
                            React.createElement(
                                "div",
                                {className: "card-action"},
                                React.createElement(
                                    "a",
                                    {href: "#"},
                                    "Mehr lesen"
                                )
                            )
                        )
                    )
                ),
                React.createElement(
                    "div",
                    {className: "row"},
                    React.createElement(
                        "div",
                        {className: "col s12 m6"},
                        React.createElement(
                            "h5",
                            null,
                            "Letzte Aktivit\xE4ten"
                        ),
                        this.state.activities && this.state.activities.length > 0 ? React.createElement(
                            "ul",
                            {className: "collection"},
                            this.state.activities.map(function (activity) {
                                return React.createElement(
                                    "li",
                                    {className: "collection-item", key: activity.id},
                                    React.createElement(
                                        "span",
                                        {className: "badge new primary-color"},
                                        activity.app
                                    ),
                                    React.createElement(
                                        "span",
                                        {className: "title"},
                                        activity.title
                                    ),
                                    React.createElement(
                                        "p",
                                        null,
                                        React.createElement(
                                            "i",
                                            {className: "material-icons left"},
                                            "access_time"
                                        ),
                                        " ",
                                        activity.created_at
                                    ),
                                    React.createElement(
                                        "p",
                                        null,
                                        activity.description
                                    )
                                );
                            })
                        ) : React.createElement(
                            "p",
                            null,
                            "Noch keine Aktivit\xE4ten vorhanden."
                        )
                    ),
                    React.createElement(
                        "div",
                        {className: "col s12 m6"},
                        React.createElement(
                            "h5",
                            null,
                            "Letzte Benachrichtigungen"
                        ),
                        this.state.notifications && this.state.notifications.length > 0 ? React.createElement(
                            "ul",
                            {className: "collection"},
                            this.state.notifications.map(function (notification) {
                                return React.createElement(
                                    "li",
                                    {className: "collection-item", key: notification.id},
                                    React.createElement(
                                        "span",
                                        {className: "badge new primary-color"},
                                        notification.app
                                    ),
                                    React.createElement(
                                        "span",
                                        {className: "title"},
                                        notification.title
                                    ),
                                    React.createElement(
                                        "p",
                                        null,
                                        React.createElement(
                                            "i",
                                            {className: "material-icons left"},
                                            "access_time"
                                        ),
                                        " ",
                                        notification.created_at
                                    ),
                                    React.createElement(
                                        "p",
                                        null,
                                        notification.description
                                    ),
                                    notification.link ? React.createElement(
                                        "p",
                                        null,
                                        React.createElement(
                                            "a",
                                            {href: notification.link},
                                            "Mehr Informationen \u2192"
                                        )
                                    ) : ""
                                );
                            })
                        ) : React.createElement(
                            "p",
                            null,
                            "Noch keine Benachrichtigungen vorhanden."
                        )
                    )
                )
            );
        }
    }]);

    return Dashboard;
}(React.Component);

$(document).ready(function () {
    var domContainer = document.querySelector('#dashboard_container');
    ReactDOM.render(React.createElement(Dashboard, null), domContainer);
});