import React from "react"

import Headline from "../components/Headline"
import BarChart from "../components/BarChart"

export default class App1Container extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      text:this.props.items[0].url+"?date=all",
      data:[5,10,1,3]
    };
  }
  PastDay(){
    this.setState({text: this.props.items[0].url+"?date=day", data:[10,15,12,23]});
  }
  PastWeek(){
    this.setState({text: this.props.items[0].url+"?date=week",data:[1,5,14,6]});
  }
  PastMonth(){
    this.setState({text: this.props.items[0].url+"?date=month",data:[60,70,65,45]});
  }
  AllTime(){
    this.setState({text: this.props.items[0].url+"?date=all",data:[5,10,1,3]});
  }
  render(){
    return(
      <div>
        <button class="btn btn-primary" onClick={() => this.PastDay()}>Past Day</button>
        <button class="btn btn-primary" onClick={() => this.PastWeek()}>Past Week</button>
        <button class="btn btn-primary" onClick={() => this.PastMonth()}>Past Month</button>
        <button class="btn btn-primary" onClick={() => this.AllTime()}>All Time</button>
        <Headline><a href={this.state.text}>test url with data {this.state.data}</a></Headline>
        <div className = 'App'>
          <div className='App-header'>
            <BarChart data={this.state.data} size={[500,500]}/>
          </div>
        </div>
      </div>

    );
  }
}
