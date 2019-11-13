const REFRESH_TIME = 15;

// function WithCheckCircleIcon(props) {
//     return <div className={"col s12"}>
//         <i className={"material-icons left green-text"}>check_circle</i>
//         {props.children}
//     </div>
// }

class Dashboard extends React.Component {
    constructor() {
        super();
        this.state = {
            refreshIn: REFRESH_TIME,
            isLoading: true
        };
    }

    updateRefreshTime = () => {
        if (this.state.refreshIn >= 1) {
            if (this.state.timeout) {
                window.clearTimeout(this.state.timeout);
            }
            const timeout = window.setTimeout(this.updateRefreshTime, 1000);
            this.setState({refreshIn: this.state.refreshIn - 1, timeout: timeout});
        } else {
            this.updateData();
        }
    };

    updateData = () => {
        const that = this;
        $.getJSON(API_URL, (data) => {
            console.log(data);
            if (data) {
                that.setState({...data, refreshIn: REFRESH_TIME + 1, isLoading: false});
                that.updateRefreshTime();
            }
        });
        $.getJSON(API_URL + "/my-plan", (data) => {
            console.log(data);
            if (data && data.lessons) {
                that.setState({lessons: data.lessons});
            }
        });
    };

    componentDidMount() {
        console.log(API_URL);
        this.updateData();
    }

    closeNotification(notification) {
        console.log(notification);
        $("#not-" + notification.id).addClass("scale-out");
        window.setTimeout(() => {
            $("#not-" + notification.id).hide();
        }, 200);
        $.getJSON(API_URL + "/notifications/read/" + notification.id);
        this.updateData();
        this.setState({time: new Date()});
    }

    render() {
        if (this.state.isLoading) {
            // Show loading screen until first data are loaded
            return <div className={"row center-via-flex container"} style={{"height": "15em"}}>
                <div className={"center2-via-flex"}>
                    <div className="preloader-wrapper big active">
                        <div className="spinner-layer spinner-primary">
                            <div className="circle-clipper left">
                                <div className="circle"/>
                            </div>
                            <div className="gap-patch">
                                <div className="circle"/>
                            </div>
                            <div className="circle-clipper right">
                                <div className="circle"/>
                            </div>
                        </div>
                    </div>
                    <p className={"text-center flow-text"}>Deine aktuellen Informationen werden geladen …</p>
                </div>
            </div>;
        }

        const that = this;
        return <div>
            {/* REFRESH BUTTON*/}
            <button className={"btn-flat right grey-text"} onClick={this.updateData}>
                <i className={"material-icons left"}>refresh</i>
                in {this.state.refreshIn} s
            </button>

            {/* GREETINGS */}
            <p className="flow-text">Moin
                Moin, {this.state.user.full_name !== "" ? this.state.user.full_name : this.state.user.username}. Hier
                findest du alle aktuellen Informationen:</p>

            <div className={"alert success"}>
                <p>
                    <i className={"material-icons left"}>report_problem</i>
                    Das neue Dashboard von SchoolApps befindet sich momentan in der <strong>Testphase</strong>. Falls
                    Fehler auftreten oder du einen Verbesserungsvorschlag für uns hast, schreibe uns bitte unter <a
                    href={"mailto:support@katharineum.de"}>support@katharineum.de</a>.
                </p>
            </div>

            {/* UNREAD NOTIFICATIONS*/}
            {this.state.unread_notifications && this.state.unread_notifications.length > 0 ?
                this.state.unread_notifications.map(function (notification) {
                    return <div className={"alert primary scale-transition"} id={"not-" + notification.id}
                                key={notification.id}>
                        <div>
                            {/* Info icon */}
                            <i className={"material-icons left"}>info</i>

                            <div className={"right"}>
                                {/* Button for marking as read*/}
                                <button className={"btn-flat"} onClick={() => that.closeNotification(notification)}>
                                    <i className={"material-icons center"}>close</i>
                                </button>
                            </div>

                            {/* Notification title and desc */}
                            <strong>{notification.title}</strong>
                            <p>{notification.description}</p>
                        </div>
                    </div>;
                }) : ""}

            {/* HINTS */}
            {this.state.plan && this.state.plan.hints.length > 0 ?
                <div>
                    {this.state.plan.hints.map(function (hint, idx) {
                        return <div className="alert primary" key={idx}>
                            <div>
                                <em className="right hide-on-small-and-down">
                                    Hinweis für {that.state.date_formatted}
                                </em>

                                <i className="material-icons left">announcement</i>
                                <p dangerouslySetInnerHTML={{__html: hint.html}}/>

                                <em className="hide-on-med-and-up">
                                    Hinweis für {that.state.date_formatted}
                                </em>
                            </div>
                        </div>;
                    })}
                </div> : ""}

            {/* CARDS */}
            <div className={"row"}>
                <div className={"dashboard-cards"}>

                    {/* MY PLAN */}
                    {this.state.has_plan ? <div className="card">
                        <div className="card-content">
                            {/* Show individualized title */}
                            <span className="card-title">
                                Plan {this.state.plan.type === 2 ? "der" : "für"} <em>
                                {this.state.plan.name}</em> für {this.state.date_formatted}
                            </span>

                            {/* Show plan */}
                            {this.state.lessons && this.state.lessons.length > 0 ? <div className={"timetable-plan"}>
                                {this.state.lessons.map(function (lesson) {
                                    // Show one lesson row
                                    return <div className="row">
                                        {/* Show time information*/}
                                        <div className="col s4">
                                            <div className="card timetable-title-card">
                                                <div className="card-content">
                                                    {/* Lesson number*/}
                                                    <span className="card-title left">
                                                        {lesson.time.number_format}
                                                    </span>

                                                    {/* Times */}
                                                    <div className="right timetable-time grey-text text-darken-2">
                                                        <span>{lesson.time.start_format}</span>
                                                        <br/>
                                                        <span>{lesson.time.end_format}</span>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>

                                        {/* Show lesson content (via generated HTML by Django) */}
                                        <div className={"col s8"} dangerouslySetInnerHTML={{__html: lesson.html}}/>
                                    </div>;
                                })}
                            </div> : ""}
                        </div>
                        <div className="card-action">
                            <a href={MY_PLAN_URL}>
                                <span className="badge new primary-color card-action-badge">SMART PLAN</span>
                                anzeigen
                            </a>
                        </div>
                    </div> : ""}

                    {/* MY STATUS */}
                    {/*<div className="card">*/}
                    {/*    <div className="card-content">*/}
                    {/*        <span className="card-title">Mein Status</span>*/}
                    {/*        <div className={"row"}>*/}
                    {/*            <WithCheckCircleIcon>*/}
                    {/*                {this.state.user_type_formatted}*/}
                    {/*            </WithCheckCircleIcon>*/}

                    {/*            {this.state.user_type === 1 || this.state.user_type === 2 ? <WithCheckCircleIcon>*/}
                    {/*                Meine Klassen: {this.state.classes.join(", ")}*/}
                    {/*            </WithCheckCircleIcon> : ""}*/}

                    {/*            {this.state.user_type === 1 || this.state.user_type === 2 ? <WithCheckCircleIcon>*/}
                    {/*                Meine Kurse: {this.state.courses.join(", ")}*/}
                    {/*            </WithCheckCircleIcon> : ""}*/}

                    {/*            {this.state.user_type === 1 ? <WithCheckCircleIcon>*/}
                    {/*                Meine Fächer: {this.state.subjects.join(", ")}*/}
                    {/*            </WithCheckCircleIcon> : ""}*/}
                    {/*            {this.state.user_type === 1 || this.state.has_wifi ?*/}
                    {/*                <WithCheckCircleIcon>WLAN</WithCheckCircleIcon> : <div className={"col"}>*/}
                    {/*                    <i className={"material-icons left red-text"}>cancel</i>*/}
                    {/*                    Kein WLAN*/}
                    {/*                </div>}*/}
                    {/*        </div>*/}
                    {/*    </div>*/}
                    {/*</div>*/}

                    {/* CURRENT EVENTS*/}
                    {this.state.current_events && this.state.current_events.length > 0 ?
                        <div className="card">
                            <div className="card-content">
                                <span className="card-title">Aktuelle Termine</span>
                                {this.state.current_events.map(function (event) {
                                    return <div className="card-panel event-card">
                                        <span className={"title"}>{event.name}</span>
                                        <br/>
                                        {event.formatted}
                                    </div>;
                                })}
                            </div>
                            <div className="card-action">
                                <a href="https://katharineum-zu-luebeck.de/aktuelles/termine/" target={"_blank"}>
                                    Weitere Termine
                                </a>
                            </div>
                        </div>
                        : ""}

                    {/* EXAMS */}
                    {/*<div className="card">*/}
                    {/*    <div className="card-content">*/}
                    {/*        <span className="card-title">Klausuren der <em>Eb</em></span>*/}
                    {/*        <div className="card-panel event-card">*/}
                    {/*            <span className={"title"}>Sextanereinschulung</span>*/}
                    {/*            <br/>*/}
                    {/*            28.Aug. 2019 18:30 - 22:00*/}
                    {/*        </div>*/}
                    {/*        <div className="card-panel event-card">*/}
                    {/*            <span className={"title"}>Sextanereinschulung</span>*/}
                    {/*            <br/>*/}
                    {/*            28.Aug. 2019 18:30 - 22:00*/}
                    {/*        </div>*/}
                    {/*    </div>*/}
                    {/*    <div className="card-action">*/}
                    {/*        <a href="https://katharineum-zu-luebeck.de/aktuelles/termine/">Alle Klausuren</a>*/}
                    {/*    </div>*/}
                    {/*</div>*/}

                    {/* NEWEST ARTICLE FROM HOMEPAGE*/}
                    {this.state.newest_article ?
                        <div>
                            <div className="card">
                                {/* Image with badge and title */}
                                <div className="card-image">
                                    <span className={"badge-image"}>Aktuelles von der Homepage</span>
                                    <img src={this.state.newest_article.image_url}
                                         alt={this.state.newest_article.title}/>
                                    <span className="card-title"
                                          dangerouslySetInnerHTML={{__html: this.state.newest_article.title}}/>
                                </div>

                                {/* Short text */}
                                <div className="card-content">
                                    <p dangerouslySetInnerHTML={{__html: this.state.newest_article.short_text}}/>
                                </div>

                                {/* Link to article */}
                                <div className="card-action">
                                    <a href={this.state.newest_article.link} target={"_blank"}>Mehr lesen</a>
                                </div>
                            </div>

                            {/* Link to homepage */}
                            <a className={"btn hundred-percent primary-color"}
                               href={"https://katharineum-zu-luebeck.de/"}
                               target={"_blank"}>
                                Weitere Artikel
                                <i className={"material-icons right"}>arrow_forward</i>
                            </a>
                        </div>
                        : ""}
                </div>
            </div>

            {/* ACITIVITIES */}
            <div className={"row"}>
                <div className="col s12 m6">
                    <h5>Letzte Aktivitäten</h5>
                    {this.state.activities && this.state.activities.length > 0 ? <ul className={"collection"}>
                        {this.state.activities.map((activity) => {
                            return <li className={"collection-item"} key={activity.id}>
                                <span className="badge new primary-color">{activity.app}</span>
                                <span className="title">{activity.title}</span>
                                <p>
                                    <i className="material-icons left">access_time</i> {activity.created_at}
                                </p>
                                <p>
                                    {activity.description}
                                </p>
                            </li>;
                        })}
                    </ul> : <p>
                        Noch keine Aktivitäten vorhanden.
                    </p>}
                </div>

                {/* NOTIFICATIONS */}
                <div className="col s12 m6">
                    <h5>Letzte Benachrichtigungen</h5>
                    {this.state.notifications && this.state.notifications.length > 0 ? <ul className={"collection"}>
                        {this.state.notifications.map((notification) => {
                            return <li className={"collection-item"} key={notification.id}>
                                <span className="badge new primary-color">{notification.app}</span>
                                <span className="title">{notification.title}</span>
                                <p>
                                    <i className="material-icons left">access_time</i> {notification.created_at}
                                </p>
                                <p>
                                    {notification.description}
                                </p>
                                {notification.link ? <p>
                                    <a href={notification.link}>Mehr Informationen →</a>
                                </p> : ""}
                            </li>;
                        })}
                    </ul> : <p>
                        Noch keine Benachrichtigungen vorhanden.
                    </p>}
                </div>
            </div>
        </div>;
    }
}

$(document).ready(function () {
    const domContainer = document.querySelector('#dashboard_container');
    ReactDOM.render(<Dashboard/>, domContainer);
});
