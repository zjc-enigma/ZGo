import { combineReducers } from "redux"

import * as actions from "./actions"
import * as logic from "./logic"

const controller = (state, action) => {
	if (state.board[action.position] != null) {
		console.log("occupied")
		return state // ignore occupied positions
	}

	if (state.ko === action.position) {
		console.log("ko")
		return state // ignore ko
	}

	let nextBoard = [
		...state.board.slice(0, action.position),
		logic.playerType(state.turn),
		...state.board.slice(action.position + 1)
	]

	let group = logic.findGroup(nextBoard, action.position)
	let deadGroups = logic.findThreatenedGroups(nextBoard, action.position).filter(g => !g.alive)
	let ko = null

	if (deadGroups.length > 0) {
		if (deadGroups.length == 1 && deadGroups[0].positions.length == 1) {
			ko = deadGroups[0].positions[0]
		}

		deadGroups.map(g => g.positions.map(p => nextBoard[p] = null))
	} else if (!group.alive) {
		console.log("suicide")
		return state // ignore suicide
	}

	return {
		...state,
		board: nextBoard,
		turn: state.turn + 1,
		ko: ko,
	}	
}

export const game = (state={}, action) => {
	switch (action.type) {
	case actions.SET_STONE:
		return controller(state, action)
	default:
		return {
			board: Array(19 * 19).fill(null),
			turn: 0,
			ko: null,
		}
	}
}

export default game