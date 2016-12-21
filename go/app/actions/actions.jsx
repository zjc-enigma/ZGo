
export const SET_STONE = "SET_STONE"


export const setStone = (position) => {
	return {
		type: SET_STONE,
		position: position
	}
}
