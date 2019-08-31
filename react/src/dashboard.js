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
            refreshIn: REFRESH_TIME
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
                that.setState({...data, refreshIn: REFRESH_TIME + 1});
                that.updateRefreshTime();
            }
        })
    };

    componentDidMount() {
        console.log(API_URL);
        this.updateData();
    }

    closeNotification(notification) {

    }

    render() {
        return <div>
            <button className={"btn-flat right grey-text"} onClick={this.updateData}>
                <i className={"material-icons left"}>refresh</i>
                in {this.state.refreshIn} s
            </button>
            <p className="flow-text">Willkommen bei SchoolApps!</p>
            <div className={"alert primary"}>
                <div>
                    <i className={"material-icons left"}>info</i>
                    <button className={"btn-flat right"}><i className={"material-icons center"}>close</i></button>
                    <strong>Ihr Antrag auf Unterrichtsbefreiung wurde genehmigt</strong>
                    <p>Ihr Antrag auf Unterrichtsbefreiung vom 20. August 2019, 08:45 Uhr bis 29. August 2019, 13:10 Uhr
                        wurde von der Schulleitung genehmigt. </p>
                </div>
            </div>
            <div className={"row"}>
                <div className={"col s12 m8"}>
                    <div className="col s12 m6">
                        <div className="card">
                            <div className="card-content">
                                <span className="card-title">Vertretungen der <em>Eb</em> für heute</span>
                                <p>I am a very simple card. I am good at containing small bits of information.
                                    I am convenient because I require little markup to use effectively.</p>
                            </div>
                            <div className="card-action">
                                <a href="#">
                                    <span className="badge new primary-color card-action-badge">SMART PLAN</span>
                                    anzeigen
                                </a>
                            </div>
                        </div>
                    </div>
                    <div className="col s12 m6">
                        <div className="card">
                            <div className="card-content">
                                <span className="card-title">Aktuelle Termine</span>
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
                                <a href="https://katharineum-zu-luebeck.de/aktuelles/termine/">Weitere Termine</a>
                            </div>
                        </div>
                    </div>


                    <div className="col s12 m6">
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


                    <div className="col s12 m6">
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

                <div className="col s12 m4">
                    <div className="card">
                        <div className="card-image">
                            <img
                                src="https://katharineum-zu-luebeck.de/wp-content/uploads/2019/08/E969562D-C413-4B18-AC63-26C768499BFF.jpeg"/>
                            <span className="card-title">Ein großer Tag - Die Einschulung der neuen Sextaner</span>
                        </div>
                        <div className="card-content">
                            <p>Am 13.08. war es wieder so weit: am Katharineum wurden die neuen Sextaner willkommen
                                geheißen. Bereits zehn Minuten vor Beginn der alljährlichen Veranstaltung war die…</p>
                        </div>
                        <div className="card-action">
                            <a href="#">Mehr lesen</a>
                        </div>
                    </div>
                </div>

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
