
import React from "react"

import { BLACK, WHITE } from "../logic/logic"

require("../css/Piece.scss")

const Piece = ({ state }) => {
	switch (state) {
	case BLACK:
		return <div className="piece">⚫</div>
	case WHITE:
		return <div className="piece">⚪️</div>
	default:
		return null
	}
}

export default Piece
