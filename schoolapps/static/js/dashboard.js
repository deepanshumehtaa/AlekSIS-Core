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
                    that.setState(Object.assign({}, data, {refreshIn: REFRESH_TIME + 1, isLoading: false}));
                    that.updateRefreshTime();
                }
            });
            $.getJSON(API_URL + "/my-plan", function (data) {
                console.log(data);
                if (data && data.lessons) {
                    that.setState({lessons: data.lessons});
                }
            });
        };

        _this.state = {
            refreshIn: REFRESH_TIME,
            isLoading: true
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
            console.log(notification);
            $("#not-" + notification.id).addClass("scale-out");
            window.setTimeout(function () {
                $("#not-" + notification.id).remove();
            }, 200);
            $.getJSON(API_URL + "/notifications/read/" + notification.id);
            this.updateData();
            this.setState({time: new Date()});
        }
    }, {
        key: "render",
        value: function render() {
            if (this.state.isLoading) {
                return React.createElement(
                    "div",
                    {className: "row center-via-flex container", style: {"height": "10em"}},
                    React.createElement(
                        "div",
                        {className: "center2-via-flex"},
                        React.createElement(
                            "div",
                            {className: "preloader-wrapper big active"},
                            React.createElement(
                                "div",
                                {className: "spinner-layer spinner-primary"},
                                React.createElement(
                                    "div",
                                    {className: "circle-clipper left"},
                                    React.createElement("div", {className: "circle"})
                                ),
                                React.createElement(
                                    "div",
                                    {className: "gap-patch"},
                                    React.createElement("div", {className: "circle"})
                                ),
                                React.createElement(
                                    "div",
                                    {className: "circle-clipper right"},
                                    React.createElement("div", {className: "circle"})
                                )
                            )
                        ),
                        React.createElement(
                            "p",
                            {className: "text-center"},
                            "Wird geladen \u2026"
                        )
                    )
                );
            }

            var that = this;
            console.log(MY_PLAN_URL);
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
                    "Moin Moin, ",
                    this.state.user.full_name !== "" ? this.state.user.full_name : this.state.user.username,
                    ". Hier findest du alle aktuellen Informationen:"
                ),
                this.state.unread_notifications && this.state.unread_notifications.length > 0 ? this.state.unread_notifications.map(function (notification) {
                    return React.createElement(
                        "div",
                        {
                            className: "alert primary scale-transition", id: "not-" + notification.id,
                            key: notification.id
                        },
                        React.createElement(
                            "div",
                            null,
                            React.createElement(
                                "i",
                                {className: "material-icons left"},
                                "info"
                            ),
                            React.createElement(
                                "div",
                                {className: "right"},
                                React.createElement(
                                    "button",
                                    {
                                        className: "btn-flat", onClick: function onClick() {
                                            return that.closeNotification(notification);
                                        }
                                    },
                                    React.createElement(
                                        "i",
                                        {className: "material-icons center"},
                                        "close"
                                    )
                                )
                            ),
                            React.createElement(
                                "strong",
                                null,
                                notification.title
                            ),
                            React.createElement(
                                "p",
                                null,
                                notification.description
                            )
                        )
                    );
                }) : "",
                React.createElement(
                    "div",
                    {className: "row"},
                    React.createElement(
                        "div",
                        {className: this.state.newest_article ? "col s12 m6 l6 xl8 no-padding" : "col s12 no-padding"},
                        React.createElement(
                            "div",
                            {className: "col s12 m12 l12 xl6"},
                            React.createElement(
                                "div",
                                {className: "card"},
                                this.state.has_plan ? React.createElement(
                                    "div",
                                    {className: "card-content"},
                                    React.createElement(
                                        "span",
                                        {className: "card-title"},
                                        "Vertretungen ",
                                        this.state.plan.type === 2 ? "der" : "für",
                                        " ",
                                        React.createElement(
                                            "em",
                                            null,
                                            this.state.plan.name
                                        ),
                                        " f\xFCr ",
                                        this.state.date_formatted
                                    ),
                                    this.state.lessons && this.state.lessons.length > 0 ? React.createElement(
                                        "div",
                                        null,
                                        this.state.lessons.map(function (lesson) {
                                            return React.createElement(
                                                "div",
                                                {className: "row"},
                                                React.createElement(
                                                    "div",
                                                    {className: "col s4"},
                                                    React.createElement(
                                                        "div",
                                                        {className: "card timetable-title-card"},
                                                        React.createElement(
                                                            "div",
                                                            {className: "card-content"},
                                                            React.createElement(
                                                                "span",
                                                                {className: "card-title left"},
                                                                lesson.time.number_format
                                                            ),
                                                            React.createElement(
                                                                "div",
                                                                {
                                                                    className: "right timetable-time grey-text text-darken-2"
                                                                },
                                                                React.createElement(
                                                                    "span",
                                                                    null,
                                                                    lesson.time.start
                                                                ),
                                                                React.createElement("br", null),
                                                                React.createElement(
                                                                    "span",
                                                                    null,
                                                                    lesson.time.end
                                                                )
                                                            )
                                                        )
                                                    )
                                                ),
                                                React.createElement("div", {
                                                    className: "col s8",
                                                    dangerouslySetInnerHTML: {__html: lesson.html}
                                                })
                                            );
                                        })
                                    ) : React.createElement(
                                        "p",
                                        null,
                                        "Keine Vertretungen f\xFCr morgen vorhanden."
                                    )
                                ) : React.createElement(
                                    "p",
                                    {className: "flow-text"},
                                    "Keine Vertretungen vorhanden."
                                ),
                                this.state.has_plan ? React.createElement(
                                    "div",
                                    {className: "card-action"},
                                    React.createElement(
                                        "a",
                                        {href: MY_PLAN_URL},
                                        React.createElement(
                                            "span",
                                            {className: "badge new primary-color card-action-badge"},
                                            "SMART PLAN"
                                        ),
                                        "anzeigen"
                                    )
                                ) : ""
                            )
                        ),
                        this.state.current_events && this.state.current_events.length > 0 ? React.createElement(
                            "div",
                            {className: "col s12 m12 l12 xl6"},
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
                                    this.state.current_events.map(function (event) {
                                        return React.createElement(
                                            "div",
                                            {className: "card-panel event-card"},
                                            React.createElement(
                                                "span",
                                                {className: "title"},
                                                event.name
                                            ),
                                            React.createElement("br", null),
                                            event.formatted
                                        );
                                    })
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
                        ) : "",
                        React.createElement(
                            "div",
                            {className: "col s12 m12 l12 xl6"},
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
                            {className: "col s12 m12 l12 xl6"},
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
                    this.state.newest_article ? React.createElement(
                        "div",
                        {className: "col s12 m6 l6 xl4"},
                        React.createElement(
                            "div",
                            {className: "card"},
                            React.createElement(
                                "div",
                                {className: "card-image"},
                                React.createElement(
                                    "span",
                                    {className: "badge-image"},
                                    "Aktuelles von der Homepage"
                                ),
                                React.createElement("img", {
                                    src: this.state.newest_article.image_url,
                                    alt: this.state.newest_article.title
                                }),
                                React.createElement("span", {
                                    className: "card-title",
                                    dangerouslySetInnerHTML: {__html: this.state.newest_article.title}
                                })
                            ),
                            React.createElement(
                                "div",
                                {className: "card-content"},
                                React.createElement("p", {dangerouslySetInnerHTML: {__html: this.state.newest_article.short_text}})
                            ),
                            React.createElement(
                                "div",
                                {className: "card-action"},
                                React.createElement(
                                    "a",
                                    {href: this.state.newest_article.link, target: "_blank"},
                                    "Mehr lesen"
                                )
                            )
                        ),
                        React.createElement(
                            "a",
                            {
                                className: "btn hundred-percent primary-color",
                                href: "https://katharineum-zu-luebeck.de/",
                                target: "_blank"
                            },
                            "Weitere Artikel",
                            React.createElement(
                                "i",
                                {className: "material-icons right"},
                                "arrow_forward"
                            )
                        )
                    ) : ""
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