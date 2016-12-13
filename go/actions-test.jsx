
jest.unmock("./actions");
import * as actions from "./actions"

describe("actions", () => {
	it("should create an action to set a stone", () => {
		const position = 1 
		expect(
			actions.setStone(position)
		).toEqual({
			type: actions.SET_STONE,
			position: position,
		})
	})
})