
jest.unmock("./logic");
import * as logic from "./logic"

describe("neighbours", () => {
	it("should create an array of neighbouring indexes", () => {
		// 1st row
		expect(logic.neighbours(0)).toEqual([1, 19])
		expect(logic.neighbours(18)).toEqual([17, 37])
		expect(logic.neighbours(1)).toEqual([0, 2, 20])

		expect(logic.neighbours(19)).toEqual([0, 20, 38])

		// Middle
		expect(logic.neighbours(180)).toEqual([161, 179, 181, 199])

		expect(logic.neighbours(341)).toEqual([322, 340, 360])

		// 19th row
		expect(logic.neighbours(342)).toEqual([323, 343])
		expect(logic.neighbours(360)).toEqual([341, 359])
		expect(logic.neighbours(343)).toEqual([324, 342, 344])
	})
})

describe("findGroup", () => {
	it("should find board groups", () => {
		expect(
			logic.findGroup(
				Array(19 * 19).fill(null).fill(0, 0, 3),
				0
			)
		).toEqual({
			alive: true,
			positions: [0, 1, 2]
		})
	})

	it("should determine if they are alive", () => {
		expect(
			logic.findGroup(
				Array(19 * 19).fill(logic.WHITE).fill(0, 0, 3),
				0
			)
		).toEqual({
			alive: false,
			positions: [0, 1, 2]
		})

		expect(
			logic.findGroup(
				Array(19 * 19).fill(logic.WHITE).fill(0, 20, 23),
				21
			)
		).toEqual({
			alive: false,
			positions: [20, 21, 22]
		})
	})
})

describe("findThreatenedGroups", () => {
	it("should find opponents groups around friendly position", () => {
		expect(
			logic.findThreatenedGroups(
				Array(19 * 19).fill(null),
				0
			)
		).toEqual([])

		expect(
			logic.findThreatenedGroups(
				Array(19 * 19).fill(null).fill(logic.BLACK, 0, 1).fill(logic.WHITE, 1, 20),
				19 // White @ 19 kill black @ 0
			)
		).toEqual([{
			alive: false,
			positions: [0]
		}])
	})
})