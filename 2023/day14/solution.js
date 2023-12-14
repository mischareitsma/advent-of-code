import * as fs from "node:fs";
import { dirname } from "path";
import { fileURLToPath } from "url";
import { Grid2D } from "../map.js";
import { sum } from "../math.js";
import { arraysAreEqual } from "../utils.js"

const __dirname = dirname(fileURLToPath(import.meta.url));

const isTest = false;
const testNumber = "";

const fname = (isTest ? `test${testNumber}_` : "") + "input.dat";

const lines = fs.readFileSync(__dirname + "/" + fname).toString().split("\n");
lines.pop();

class Rock {
	x = 0;
	y = 0;
	value = "";
	hasMoved = false;
	northLoad = [];

	constructor(x, y, value) {
		this.x = x;
		this.y = y;
		this.value = value;
	}

	finishedMoving() {
		this.hasMoved = true;
		this.northLoad.push(this.y + 1);
	}
}

const TILES = {
	empty: ".",
	roundRock: "O",
	cubeRock: "#",
}

// Directions are DIR: [dx, dy];
const DIRECTION = {
	NORTH: {
		delta: [0, 1],
		isFurther: (x1, y1, x2, y2) => y1 >= y2,
		sorter: (x1, y1, x2, y2) => y1 - y2,
	},
	WEST: {
		delta: [-1, 0],
		isFurther: (x1, y1, x2, y2) => x1 <= x2,
		sorter: (x1, y1, x2, y2) => x2 - x1,
	},
	EAST: {
		delta: [1, 0],
		isFurther: (x1, y1, x2, y2) => x1 >= x2,
		sorter: (x1, y1, x2, y2) => x1 - x2,
	},
	SOUTH: {
		delta: [0, -1],
		isFurther: (x1, y1, x2, y2) => y1 <= y2,
		sorter: (x1, y1, x2, y2) => y2 - y1,
	}
}

const DIRECTIONS = ["NORTH", "WEST", "SOUTH", "EAST"];

const rocks = [];

const platform = new Grid2D(lines[0].length, lines.length);

lines.forEach( (line, iy) => {
	Array.from(line).forEach((char, ix) => {
		platform.setValue(ix, platform.width - iy - 1, char);
	});
});

platform.values.forEach((v, idx) => {
	if (v === TILES.roundRock) {
		const [x, y] = platform.getCoords(idx)
		rocks.push(new Rock(x, y, v));
	}
});


function tiltDirection(direction) {
	if (!(direction in DIRECTION))
		throw new Error(`Invalid direction ${direction}`);

	const [dx, dy] = DIRECTION[direction].delta;
	const sorter = DIRECTION[direction].sorter;


	let rocksStuck = rocks.length;

	while (rocksStuck--) {
		// TODO: Sorting takes time, might want to just copy the list and
		// prune. Also, the reason why the initial run didn't work might be a bug.
		const availableRocks = rocks
			.filter(r => !r.hasMoved)
			.sort((r1, r2) => sorter(r1.x, r1.y, r2.x, r2.y));
		const rock = availableRocks.at(-1);
		moveRock(rock, dx, dy);
		rock.finishedMoving();
	}

	rocks.forEach(r => {r.hasMoved = false;})
}

/**
 * Move rock on the platform.
 * 
 * @param {Rock} r Rock to move
 * @param {number} dx x direction
 * @param {number} dy y direction
 */
function moveRock(r, dx, dy) {
	const canMove = () => {
		const x = r.x + dx;
		const y = r.y + dy
		if (!platform.validCoords(x, y))
			return false;

		if (platform.getValue(x, y) !== TILES.empty)
			return false;

			return true;
	}

	while (canMove()) {
		platform.setValue(r.x, r.y, TILES.empty);
		platform.setValue(r.x + dx, r.y + dy, TILES.roundRock);
		r.x += dx
		r.y += dy
	}
}

const totalLoad = [];

let cycles = 0;

let pattern = [];

function getPattern() {
	// Some constants in this function:

	// Really need some cycles to find a pattern, return [] otherwise
	const minimumCycles = 2;

	// Limit how big a pattern can be. The test pattern was only 7 cycles = 7*2 = 14 entries
	const maxPatternSize = 1000;

	const pattern = [];

	if (cycles < minimumCycles) return pattern;

	const currentIdx = totalLoad.length - 1
	const currentLoad = totalLoad[currentIdx];

	let prevValIdx = totalLoad.lastIndexOf(currentLoad, currentIdx-1);


	while ((currentIdx - prevValIdx < maxPatternSize)) {
		let isPattern = true;

		for (let i = 0; i < (currentIdx - prevValIdx) && isPattern; i++) {
			isPattern = (totalLoad[currentIdx-i] === totalLoad[prevValIdx-i]);
		}

		if (isPattern) break;

		prevValIdx = totalLoad.lastIndexOf(currentLoad, prevValIdx - 1);
		if (prevValIdx === -1) return [];
	}

	// Do slice etc. for now this works.
	for (let i = 0; i < (currentIdx - prevValIdx); i++) {
		pattern.push(totalLoad[prevValIdx + i + 1]);
	}

	return pattern;
}

while (!pattern.length) {

	const start = Date.now();

	for (const direction of DIRECTIONS) {
		// TODO: we are done if the loads of one cycle stay the same as the previous ones.
		tiltDirection(direction);
		// Load stays the same if we go east or west, so just add after north or south.
		// TODO: Maybe check for pattern per rock?
		if (direction === "NORTH" || direction === "SOUTH")
			totalLoad.push(sum(rocks.map(r => r.y + 1)));
	}

	console.log(`Cycle ${cycles} took ${Date.now() - start} ms`);

	cycles++;
	pattern = getPattern();
}

console.log(`Took ${cycles} cycles`);
console.log(`Current load: ${totalLoad.at(-1)}`);
console.log("Pattern: ", pattern);

const actualPattern = [];
pattern.forEach(v => actualPattern.push(v, v));

console.log("Actual pattern", actualPattern);

const TOTAL_CYCLES = 1000000000;
const remainder = TOTAL_CYCLES - cycles;
const remainderTilts = remainder * 4;
const remainderTiltsModPattern = remainderTilts % actualPattern.length;

const loadAfterAllCycles = actualPattern[remainderTiltsModPattern - 1];

function part1() {
	return totalLoad[0];
}

function part2() {
	// not 94831
	return loadAfterAllCycles;
}

function main() {
	console.log(`Part 1: ${part1()}`);
	console.log(`Part 2: ${part2()}`);
}

main();
