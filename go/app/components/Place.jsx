
import React from "react"
import { Component } from "react"

import Piece from "./Piece"
import { BOARD_SIZE } from "../constants/constants"

let A = 0
let B = BOARD_SIZE - 1
let C = BOARD_SIZE * (BOARD_SIZE - 1)
let D = BOARD_SIZE * BOARD_SIZE - 1

const classBackground = (index) => {
	switch (index) {
	case A:
		return "corner-tl"
	case B:
		return "corner-tr"
	case C:
		return "corner-bl"
	case D:
		return "corner-br"
	case 60: case 66: case 72:
	case 174: case 180: case 186:
	case 288: case 294: case 300:
		return "special"
	default:
	}

	switch (true) {
	case (A < index && index < B):
		return "side-t"
	case (C < index && index < D):
		return "side-b"
	default:
	}

	switch (0) {
	case (index % BOARD_SIZE):
		return "side-l"
	case ((index + 1) % BOARD_SIZE):
		return "side-r"
	}

	return null
}

class Place extends Component {
	render() {
		let { index, state, onClick } = this.props
		let classNames = ["place", classBackground(index)].join(' ')

		return (
			<div className={classNames} onClick={onClick}>
				<Piece state={state} />
			</div>
		)
	}
}

export default Place
