import React from "react"
import { Component } from "react"
import { connect } from "react-redux"

import * as actions from "../actions/actions"
import Place from "./Place"

require("../css/board.scss")


export class Board extends Component {

  constructor(props, context){
    super(props, context)
  }


  updateBoard(json) {
    console.log('updateBoard:', json)
    this.props.dispatch({
      type: "UPDATE_BOARD",
      pos: json.pos
    })
  }

  getNextBoard(pos) {
    
    console.log('action.position:', pos)
    fetch("/get_next_move",
      {method: 'POST',
        headers:{
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({position: pos})
      })
      .then(res => res.json())
      .then(json => this.updateBoard(json))
      .catch(e => {console.log('/get_next_move failed', e)})
  }



	render() {
		console.log("PROPS: ", this.props)
    let { board, dispatch, turn } = this.props
		return (
			<div className="board">
				{ board.map((s, i) => 
					          <Place key={i} index={i} state={s} onClick={ () => {
                      this.getNextBoard(i)
                    }}/>
				)}
			</div>
		)
	}
}
export default connect(state => state)(Board)
