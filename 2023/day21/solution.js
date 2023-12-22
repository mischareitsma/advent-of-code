import { readFileSync } from "node:fs";
import { dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { Grid2D } from "../map.js";

const __dirname = dirname(fileURLToPath(import.meta.url));

const isTest = false;
const testNumber = "";

const fname = (isTest ? `test${testNumber}_` : "") + "input.dat";

const lines = readFileSync(__dirname + "/" + fname).toString().split("\n");
lines.pop();

const TILES = {
	garden: ".",
	start: "S",
	rock: "#"
}

const STEPS = isTest ? 6 : 64; // Steps for part 1
const DIRECTIONS = [[1, 0], [-1, 0], [0, 1], [0, -1]];

const map = Grid2D.from_lines(lines);

const START = map.getCoords(map.values.indexOf(TILES.start));

function part1_naive() {
	let steps = STEPS;
	let locations = [START.join(",")];
	while (steps--) {
		const newLocations = [];

		locations.forEach(location => {
			// Need to parseInt every time, maybe still two maps are better, one
			// with string to check (could be a set) and the other with the actual
			// coords.
			// Other option: Could also just make a stepsMap...
			const [x, y] = location.split(",").map(e => Number.parseInt(e));

			DIRECTIONS.forEach(dir => {
				const [dx, dy] = dir;
				const xn = x + dx;
				const yn = y + dy;
				const coords = `${xn},${yn}`

				if (newLocations.includes(coords))
					return;

				if (!map.validCoords(xn, yn))
					return;

				if (map.getValue(xn, yn) === TILES.rock)
					return;

				newLocations.push(coords);
			});
		});
		locations = newLocations;
	}
	return locations.length;
}

const DELTAS = [
	{dx: 0, dy: 1},
	{dx: -1, dy: 0},
	{dx: 1, dy: 0},
	{dx: 0, dy: -1}
];

function getPlotsAfterSteps(steps) {
	let currentMap = map.copy();

	currentMap.setValue(START[0], START[1], "O");
	const possiblePlots = [];

	const TOTAL_STEPS = steps;

	while (steps--) {
		const stepsMap = map.copy();
		currentMap.values.forEach((steppedOn, idx) => {
			if (steppedOn !== "O") return;
	
			const [x, y] = currentMap.getCoords(idx);
	
			DELTAS.forEach(delta => {
				const xn = x + delta.dx;
				const yn = y + delta.dy;
	
				if (!currentMap.validCoords(xn, yn)) return;
				if (currentMap.getValue(xn, yn) === "#") return;
	
				stepsMap.setValue(xn, yn, "O");
			});
		});

		currentMap = stepsMap.copy();
		possiblePlots.push(currentMap.values.filter(v => v === "O").length)
		console.log(`After ${TOTAL_STEPS - steps} steps we have ${possiblePlots.at(-1)} positions`);
		if (possiblePlots.length >= 5 && possiblePlots.at(-3) === possiblePlots.at(-1) && possiblePlots.at(-1) === possiblePlots.at(-5)) break;
	}

	/* It oscillates between two values, for the test map 42 and 39
	
	Possible algo:
	- For all boundary points, check how many steps it takes to get oscillation and which value
	- For all boundary points, get shortest paths to other edges
	- For start position, get shortest paths to boundaries
	- Condense the infinite map pattern to a map itself, where each element is a copy of the "map", size is naively (STEPS / shortest route left right or up down) ** 2?
	  check note before, probably not or only for a few maps around the original
	- Calculate for the boundaries the number of steps it takes to get to oscillation, and what
	  the initial oscillation value would be.


	Extra note:
	At a certain moment the shortest routes are the "highways" between maps, so the height or
	width of the map. Those "routes" will catch up on alternate routes rather quickly, seeing
	that the map is only 131 x 131 and the number iof steps is many orders of magnitude larger.
	So then it just becomes a matter of calculating after how many steps we get to the corners
	of the original map. And for a few maps around us we still need to keep track of how fast
	we get there I think, because the oscillation might be offset.
	*/
	
	return 0;
}

function part1() {
	getPlotsAfterSteps(50);
}

function part2() {
	const testInput = [6, 10, 50, 100, 500, 1000, 5000];
	const testResult = [16, 50, 1594, 6536, 167004, 668697, 16733044];
	/**
	 * In exactly 6 steps, he can still reach 16 garden plots.
	In exactly 10 steps, he can reach any of 50 garden plots.
	In exactly 50 steps, he can reach 1594 garden plots.
	In exactly 100 steps, he can reach 6536 garden plots.
	In exactly 500 steps, he can reach 167004 garden plots.
	In exactly 1000 steps, he can reach 668697 garden plots.
	In exactly 5000 steps, he can reach 16733044 garden plots.
	 */
	if (isTest) {
		testInput.forEach((steps, idx) => {
			logResult(`2.${idx}`, getPlotsAfterSteps(steps), testResult[idx]);
		});

	}
	else {
		logResult(2, getPlotsAfterSteps(26501365), "N/A");
	}
	return "";
}

function logResult(part, result, testResult) {
	console.log(
		`Part ${part}: ${result} (test${testNumber}` +
		`${!isTest ? "" : testResult === result ? " OK" : " NOK"}: ${testResult})`
	);

}

function main() {
	// logResult(1, part1(), 16);
	// part2();
	getPlotsAfterSteps(5000)
}

main();
