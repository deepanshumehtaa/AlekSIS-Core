const REFRESH_TIME = 15;

function WithCheckCircleIcon(props) {
    return <div className={"col s12"}>
        <i className={"material-icons left green-text"}>check_circle</i>
        {props.children}
    </div>
}

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
            console.log("WOrk");
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
        })
    };

    componentDidMount() {
        console.log(API_URL);
        this.updateData();
    }

    closeNotification(notification) {
        console.log(notification);
        $("#not-" + notification.id).addClass("scale-out");
        window.setTimeout(() => {
            $("#not-" + notification.id).remove();
        }, 200);
        $.getJSON(API_URL + "/notifications/read/" + notification.id);
        this.updateData();
        this.setState({time: new Date()});
    }

    render() {
        if (this.state.isLoading) {
            return <div className={"row center-via-flex container"} style={{"height": "10em"}}>
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
                    <p className={"text-center"}>Wird geladen …</p>
                </div>
            </div>;
        }

        const that = this;
        console.log(MY_PLAN_URL);
        return <div>
            <button className={"btn-flat right grey-text"} onClick={this.updateData}>
                <i className={"material-icons left"}>refresh</i>
                in {this.state.refreshIn} s
            </button>
            <p className="flow-text">Willkommen bei SchoolApps!</p>
            {this.state.unread_notifications && this.state.unread_notifications.length > 0 ?
                this.state.unread_notifications.map(function (notification) {
                    return <div className={"alert primary scale-transition"} id={"not-" + notification.id}
                                key={notification.id}>
                        <div>
                            <i className={"material-icons left"}>info</i>
                            <div className={"right"}>
                                <button className={"btn-flat"} onClick={() => that.closeNotification(notification)}>
                                    <i className={"material-icons center"}>close</i>
                                    {/*Gelesen*/}
                                </button>
                            </div>
                            <strong>{notification.title}</strong>
                            <p>{notification.description}</p>
                        </div>
                    </div>;
                }) : ""}

            <div className={"row"}>
                <div className={"col s12 m6 l6 xl8 no-padding"}>
                    <div className="col s12 m12 l12 xl6">
                        <div className="card">
                            {this.state.has_plan ? <div className="card-content">
                                <span className="card-title">Vertretungen {this.state.plan.type == 2 ? "der" : "für"}
                                    <em>{this.state.plan.name}</em> für {this.state.date_formatted}</span>
                                <p>Keine Vertretungen für morgen vorhanden.</p>
                            </div> : <p className={"flow-text"}>Keine Vertretungen vorhanden.</p>}
                            {this.state.has_plan ? <div className="card-action">
                                <a href={MY_PLAN_URL}>
                                    <span className="badge new primary-color card-action-badge">SMART PLAN</span>
                                    anzeigen
                                </a>
                            </div> : ""}
                        </div>
                    </div>
                    <div className="col s12 m12 l12 xl6">
                        <div className="card">
                            <div className="card-content">
                                <span className="card-title">Aktuelle Termine</span>
                                {this.state.current_events && this.state.current_events.length > 0 ? this.state.current_events.map(function (event) {
                                    return <div className="card-panel event-card">
                                        <span className={"title"}>{event.name}</span>
                                        <br/>
                                        {event.formatted}
                                    </div>;
                                }) : "Keine aktuellen Termine"}
                            </div>
                            <div className="card-action">
                                <a href="https://katharineum-zu-luebeck.de/aktuelles/termine/">Weitere Termine</a>
                            </div>
                        </div>
                    </div>


                    <div className="col s12 m12 l12 xl6">
                        <div className="card">
                            <div className="card-content">
                                <span className="card-title">Mein Status</span>
                                <div className={"row"}>
                                    <WithCheckCircleIcon>
                                        {this.state.user_type_formatted}
                                    </WithCheckCircleIcon>

                                    {this.state.user_type === 1 || this.state.user_type === 2 ? <WithCheckCircleIcon>
                                        Meine Klassen: {this.state.classes.join(", ")}
                                    </WithCheckCircleIcon> : ""}

                                    {this.state.user_type === 1 || this.state.user_type === 2 ? <WithCheckCircleIcon>
                                        Meine Kurse: {this.state.courses.join(", ")}
                                    </WithCheckCircleIcon> : ""}

                                    {this.state.user_type === 1 ? <WithCheckCircleIcon>
                                        Meine Fächer: {this.state.subjects.join(", ")}
                                    </WithCheckCircleIcon> : ""}
                                    {this.state.user_type === 1 || this.state.has_wifi ?
                                        <WithCheckCircleIcon>WLAN</WithCheckCircleIcon> : <div className={"col"}>
                                            <i className={"material-icons left red-text"}>cancel</i>
                                            Kein WLAN
                                        </div>}
                                </div>
                            </div>
                        </div>
                    </div>


                    <div className="col s12 m12 l12 xl6">
                        <div className="card">
                            <div className="card-content">
                                <span className="card-title">Klausuren der <em>Eb</em></span>
                                <div className="card-panel event-card">
                                    <span className={"title"}>Sextanereinschulung</span>
                                    <br/>
                                    28.Aug. 2019 18:30 - 22:00
                                </div>
                                <div className="card-panel event-card">
                                    <span className={"title"}>Sextanereinschulung</span>
                                    <br/>
                                    28.Aug. 2019 18:30 - 22:00
                                </div>
                            </div>
                            <div className="card-action">
                                <a href="https://katharineum-zu-luebeck.de/aktuelles/termine/">Alle Klausuren</a>
                            </div>
                        </div>
                    </div>
                </div>

                {this.state.newest_article ? <div className="col s12 m6 l6 xl4">
                    <div className="card">
                        <div className="card-image">
                            <span className={"badge-image"}>Aktuelles von der Homepage</span>
                            <img src={this.state.newest_article.image_url} alt={this.state.newest_article.title}/>
                            <span className="card-title"
                                  dangerouslySetInnerHTML={{__html: this.state.newest_article.title}}/>
                        </div>
                        <div className="card-content">
                            <p dangerouslySetInnerHTML={{__html: this.state.newest_article.short_text}}/>
                        </div>
                        <div className="card-action">
                            <a href={this.state.newest_article.link} target={"_blank"}>Mehr lesen</a>
                        </div>
                    </div>
                    <a className={"btn hundred-percent primary-color"} href={"https://katharineum-zu-luebeck.de/"}
                       target={"_blank"}>
                        Weitere Artikel
                        <i className={"material-icons right"}>arrow_forward</i>
                    </a>
                </div> : ""}

            </div>
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
