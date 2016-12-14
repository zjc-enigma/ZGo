
import React from "react"
import { Component } from "react"
import { connect } from "react-redux"

import * as actions from "../actions/actions"
import Place from "./Place"

require("../css/board.scss")

export class Board extends Component {
	render() {
		let { board, dispatch, turn } = this.props
		console.log("PROPS: ", this.props)
		return (
			<div className="board">
				{ board.map((s, i) => 
					<Place key={i} index={i} state={s} onClick={() => {
						dispatch(actions.setStone(i, turn))
					}}/>
				)}
			</div>
		)
	}
}

export default connect(state => state)(Board)
