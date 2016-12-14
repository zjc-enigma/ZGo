// @flow
import { BOARD_SIZE, BOARD_SIZE_2 } from "../constants/constants"

export const BLACK: boolean = false
export const WHITE: boolean = true

// Debug board view to console
export const boardPrint = (board: boolean[]) => {
	console.log(board.map(t => {
		switch (t) {
		case BLACK:
			return '0'
		case WHITE:
			return 'O'
		default:
			return '-'
		}
	}).reduce((s, v, i) => (
		s + v + ((i + 1) % BOARD_SIZE === 0 ? '\n' : ' ')
	), ''))
}

// Returns the boolean representation of player;
// false == 'black' or true == 'white'
export const playerType = (turn: number): boolean => (
	!!(turn % 2)
)

// Creates an array of neighbouring positions
export const neighbours = (position: number): number[] => {
	let nbs: number[] = []
	if (position >= BOARD_SIZE) {
		nbs.push(position - BOARD_SIZE)
	}
	if ((position % BOARD_SIZE) !== 0) {
		nbs.push(position - 1)
	}
	if (((position + 1) % BOARD_SIZE) !== 0) {
		nbs.push(position + 1)
	}
	if (position < (BOARD_SIZE * (BOARD_SIZE - 1))) {
		nbs.push(position + BOARD_SIZE)
	}

	return nbs
}

type Group = {positions: number[], alive: boolean};

// Finds the board group belonging to a given piece
export const findGroup = (board: boolean[], position: number): Group => {
	let group: Group = {
		positions: [],
		alive: false
	}

	let type = board[position]
	if (type === null) {
		return group
	}
	
	// Mutating search
	let search: number[] = [position]
	for (let i: number = 0; search[i] !== undefined; i++) {
		let p = search[i]
		let t = board[p]

		if (t === type) {
			group.positions.push(p)
			search.push(
				...neighbours(p).filter(x => !search.includes(x))
			)
		} else if (t === null) {
			group.alive = true
		}
	}

	group.positions.sort()
	return group
}

// Finds the oppenents groups around a friendly position
export const findThreatenedGroups = (board: boolean[], position: number): Group[] => {
	let type: boolean = !board[position] // opponents type
	let positions: number[] = neighbours(position).filter(i => board[i] === type)
	let groups: Group[] = []

	for (let i = positions.length - 1; i >= 0; i--) {
		let p = positions[i]

		if (groups.reduce((s, g) => (
			s || g.positions.includes(p)
		), false)) {
			continue // skip duplicate groups
		}

		groups.push(findGroup(board, p))
	}

	return groups
}
