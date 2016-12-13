
jest.unmock("./actions");
jest.unmock("./reducers");

import reducer from "./reducers"
import * as actions from "./actions"
import * as reducers from "./reducers"

describe("game reducer", () => {
	it('should return the inital state', () => {
		expect(reducer(undefined, {})).toBeTruthy()
	})
})