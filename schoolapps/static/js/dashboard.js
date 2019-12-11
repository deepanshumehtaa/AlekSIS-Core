var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var REFRESH_TIME = 15;

// function WithCheckCircleIcon(props) {
//     return <div className={"col s12"}>
//         <i className={"material-icons left green-text"}>check_circle</i>
//         {props.children}
//     </div>
// }

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
                _this.setState({ refreshIn: _this.state.refreshIn - 1, timeout: timeout });
            } else {
                _this.updateData();
            }
        };

        _this.updateData = function () {
            var that = _this;
            $.getJSON(API_URL, function (data) {
                console.log(data);
                if (data) {
                    that.setState(Object.assign({}, data, { refreshIn: REFRESH_TIME + 1, isLoading: false }));
                    that.updateRefreshTime();
                }
            });
            $.getJSON(API_URL + "/my-plan", function (data) {
                console.log(data);
                if (data && data.lessons) {
                    that.setState({ lessons: data.lessons, holiday: data.holiday });
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
                $("#not-" + notification.id).hide();
            }, 200);
            $.getJSON(API_URL + "/notifications/read/" + notification.id);
            this.updateData();
            this.setState({ time: new Date() });
        }
    }, {
        key: "render",
        value: function render() {
            if (this.state.isLoading) {
                // Show loading screen until first data are loaded
                return React.createElement(
                    "div",
                    { className: "row center-via-flex container", style: { "height": "15em" } },
                    React.createElement(
                        "div",
                        { className: "center2-via-flex" },
                        React.createElement(
                            "div",
                            { className: "preloader-wrapper big active" },
                            React.createElement(
                                "div",
                                { className: "spinner-layer spinner-primary" },
                                React.createElement(
                                    "div",
                                    { className: "circle-clipper left" },
                                    React.createElement("div", { className: "circle" })
                                ),
                                React.createElement(
                                    "div",
                                    { className: "gap-patch" },
                                    React.createElement("div", { className: "circle" })
                                ),
                                React.createElement(
                                    "div",
                                    { className: "circle-clipper right" },
                                    React.createElement("div", { className: "circle" })
                                )
                            )
                        ),
                        React.createElement(
                            "p",
                            { className: "text-center flow-text" },
                            "Deine aktuellen Informationen werden geladen \u2026"
                        )
                    )
                );
            }

            var that = this;
            return React.createElement(
                "div",
                null,
                React.createElement(
                    "button",
                    { className: "btn-flat right grey-text", onClick: this.updateData },
                    React.createElement(
                        "i",
                        { className: "material-icons left" },
                        "refresh"
                    ),
                    "in ",
                    this.state.refreshIn,
                    " s"
                ),
                React.createElement(
                    "p",
                    { className: "flow-text" },
                    "Moin Moin, ",
                    this.state.user.full_name !== "" ? this.state.user.full_name : this.state.user.username,
                    ". Hier findest du alle aktuellen Informationen:"
                ),
                React.createElement(
                    "div",
                    { className: "alert success" },
                    React.createElement(
                        "p",
                        null,
                        React.createElement(
                            "i",
                            { className: "material-icons left" },
                            "report_problem"
                        ),
                        "Das neue Dashboard von SchoolApps befindet sich momentan in der ",
                        React.createElement(
                            "strong",
                            null,
                            "Testphase"
                        ),
                        ". Falls Fehler auftreten oder du einen Verbesserungsvorschlag f\xFCr uns hast, schreibe uns bitte unter ",
                        React.createElement(
                            "a",
                            {
                                href: "mailto:support@katharineum.de" },
                            "support@katharineum.de"
                        ),
                        "."
                    )
                ),
                this.state.unread_notifications && this.state.unread_notifications.length > 0 ? this.state.unread_notifications.map(function (notification) {
                    return React.createElement(
                        "div",
                        { className: "alert primary scale-transition", id: "not-" + notification.id,
                            key: notification.id },
                        React.createElement(
                            "div",
                            null,
                            React.createElement(
                                "i",
                                { className: "material-icons left" },
                                "info"
                            ),
                            React.createElement(
                                "div",
                                { className: "right" },
                                React.createElement(
                                    "button",
                                    { className: "btn-flat", onClick: function onClick() {
                                            return that.closeNotification(notification);
                                        } },
                                    React.createElement(
                                        "i",
                                        { className: "material-icons center" },
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
                this.state.plan && this.state.plan.hints.length > 0 ? React.createElement(
                    "div",
                    null,
                    this.state.plan.hints.map(function (hint, idx) {
                        return React.createElement(
                            "div",
                            { className: "alert primary", key: idx },
                            React.createElement(
                                "div",
                                null,
                                React.createElement(
                                    "em",
                                    { className: "right hide-on-small-and-down" },
                                    "Hinweis f\xFCr ",
                                    that.state.date_formatted
                                ),
                                React.createElement(
                                    "i",
                                    { className: "material-icons left" },
                                    "announcement"
                                ),
                                React.createElement("p", { dangerouslySetInnerHTML: { __html: hint.html } }),
                                React.createElement(
                                    "em",
                                    { className: "hide-on-med-and-up" },
                                    "Hinweis f\xFCr ",
                                    that.state.date_formatted
                                )
                            )
                        );
                    })
                ) : "",
                React.createElement(
                    "div",
                    { className: "row" },
                    this.state.has_plan ? React.createElement(
                        "div",
                        {className: "col s12 m12 l6 xl4"},
                        React.createElement(
                            "div",
                            {className: "card"},
                            React.createElement(
                                "div",
                                {className: "card-content"},
                                React.createElement(
                                    "span",
                                    {className: "card-title"},
                                    "Plan ",
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
                                this.state.holiday ? React.createElement(
                                    "div",
                                    { className: "card" },
                                    React.createElement(
                                        "div",
                                        { className: "card-content" },
                                        React.createElement(
                                            "span",
                                            {
                                                className: "badge new blue center-align holiday-badge" },
                                            this.state.holiday.name
                                        ),
                                        React.createElement("br", null)
                                    )
                                ) : this.state.lessons && this.state.lessons.length > 0 ? React.createElement(
                                    "div",
                                    { className: "timetable-plan" },
                                    this.state.lessons.map(function (lesson) {
                                        // Show one lesson row
                                        return React.createElement(
                                            "div",
                                            { className: "row" },
                                            React.createElement(
                                                "div",
                                                { className: "col s4" },
                                                React.createElement(
                                                    "div",
                                                    { className: "card timetable-title-card" },
                                                    React.createElement(
                                                        "div",
                                                        { className: "card-content" },
                                                        React.createElement(
                                                            "span",
                                                            { className: "card-title left" },
                                                            lesson.time.number_format
                                                        ),
                                                        React.createElement(
                                                            "div",
                                                            {
                                                                className: "right timetable-time grey-text text-darken-2" },
                                                            React.createElement(
                                                                "span",
                                                                null,
                                                                lesson.time.start_format
                                                            ),
                                                            React.createElement("br", null),
                                                            React.createElement(
                                                                "span",
                                                                null,
                                                                lesson.time.end_format
                                                            )
                                                        )
                                                    )
                                                )
                                            ),
                                            React.createElement("div", { className: "col s8",
                                                dangerouslySetInnerHTML: { __html: lesson.html } })
                                        );
                                    })
                                ) : ""
                            ),
                            React.createElement(
                                "div",
                                { className: "card-action" },
                                React.createElement(
                                    "a",
                                    { href: MY_PLAN_URL },
                                    React.createElement(
                                        "span",
                                        { className: "badge new primary-color card-action-badge" },
                                        "SMART PLAN"
                                    ),
                                    "anzeigen"
                                )
                            )
                        )
                    ) : "",
                    this.state.current_events && this.state.current_events.length > 0 ? React.createElement(
                        "div",
                        {className: "col s12 m12 l6 xl4"},
                        React.createElement(
                            "div",
                            {className: "card "},
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
                                        { className: "card-panel event-card" },
                                        React.createElement(
                                            "span",
                                            { className: "title" },
                                            event.name
                                        ),
                                        React.createElement("br", null),
                                        event.formatted
                                    );
                                })
                            ),
                            React.createElement(
                                "div",
                                { className: "card-action" },
                                React.createElement(
                                    "a",
                                    { href: "https://katharineum-zu-luebeck.de/aktuelles/termine/", target: "_blank" },
                                    "Weitere Termine"
                                )
                            )
                        )
                    ) : "",
                    this.state.newest_article ? React.createElement(
                        "div",
                        {className: "col s12 m12 l6 xl4"},
                        React.createElement(
                            "div",
                            {className: "card"},
                            React.createElement(
                                "div",
                                {className: "card-image"},
                                React.createElement(
                                    "span",
                                    {className: "badge-image z-depth-2"},
                                    "Aktuelles von der Homepage"
                                ),
                                React.createElement("img", {
                                    src: this.state.newest_article.image_url,
                                    alt: this.state.newest_article.title
                                })
                            ),
                            React.createElement(
                                "div",
                                {className: "card-content"},
                                React.createElement("span", {
                                    className: "card-title",
                                    dangerouslySetInnerHTML: {__html: this.state.newest_article.title}
                                }),
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
                    { className: "row" },
                    React.createElement(
                        "div",
                        { className: "col s12 m6" },
                        React.createElement(
                            "h5",
                            null,
                            "Letzte Aktivit\xE4ten"
                        ),
                        this.state.activities && this.state.activities.length > 0 ? React.createElement(
                            "ul",
                            { className: "collection" },
                            this.state.activities.map(function (activity) {
                                return React.createElement(
                                    "li",
                                    { className: "collection-item", key: activity.id },
                                    React.createElement(
                                        "span",
                                        { className: "badge new primary-color" },
                                        activity.app
                                    ),
                                    React.createElement(
                                        "span",
                                        { className: "title" },
                                        activity.title
                                    ),
                                    React.createElement(
                                        "p",
                                        null,
                                        React.createElement(
                                            "i",
                                            { className: "material-icons left" },
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
                        { className: "col s12 m6" },
                        React.createElement(
                            "h5",
                            null,
                            "Letzte Benachrichtigungen"
                        ),
                        this.state.notifications && this.state.notifications.length > 0 ? React.createElement(
                            "ul",
                            { className: "collection" },
                            this.state.notifications.map(function (notification) {
                                return React.createElement(
                                    "li",
                                    { className: "collection-item", key: notification.id },
                                    React.createElement(
                                        "span",
                                        { className: "badge new primary-color" },
                                        notification.app
                                    ),
                                    React.createElement(
                                        "span",
                                        { className: "title" },
                                        notification.title
                                    ),
                                    React.createElement(
                                        "p",
                                        null,
                                        React.createElement(
                                            "i",
                                            { className: "material-icons left" },
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
                                            { href: notification.link },
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