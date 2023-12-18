import { readFileSync } from "node:fs";
import { dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { sort } from "../math.js";

const __dirname = dirname(fileURLToPath(import.meta.url));

const isTest = true;
const testNumber = "";

const fname = (isTest ? `test${testNumber}_` : "") + "input.dat";

const lines = readFileSync(__dirname + "/" + fname).toString().split("\n");
lines.pop();

const DIRECTIONS = ["R", "D", "L", "U"];

const smallLagoonInstructions = [];
const largeLagoonInstructions = []

lines.forEach(l => {
	const [p1, p2, p3] = l.split(" ");

	smallLagoonInstructions.push({direction: p1, steps: Number.parseInt(p2)})
	largeLagoonInstructions.push({
		direction: DIRECTIONS[Number.parseInt(p3.slice(7, 8))],
		steps: Number.parseInt(p3.slice(2, 7), 16)
	});
});

class LagoonMap {

	size = 0;
	min = {x: 1e99, y: 1e99}
	max = {x: -1e99, y: -1e99}
	pos = {x: 0, y: 0}
	
	lines = {
		"R": [],
		"L": [],
		"U": [],
		"D": []
	}

	constructor(instructions) {
		this.instructions = instructions;
	}

	updateCoordinates(vec) {
		vec.forEach(v => {
			this.updateMinCoords(v);
			this.updateMaxCoords(v);
		});
	}

	updateMinCoords(vec) {
		if (vec.x < this.min.x)
			this.min.x = vec.x;
		if (vec.y < this.min.y)
			this.min.y = vec.y
	}

	updateMaxCoords(vec) {
		if (vec.x > this.max.x)
			this.max.x = vec.x;
		if (vec.y > this.max.y)
			this.max.y = vec.y
	}

	getDeltaFromInstruction(instruction) {
		switch (instruction.direction) {
			case "R":
				return {x: instruction.steps, y: 0};
			case "L":
				return {x: -instruction.steps, y: 0};
			case "U":
				return {x: 0, y: instruction.steps};
			case "D":
				return {x: 0, y: -instruction.steps};
		}

		throw new Error("Invalid direction " + instruction.direction);
	}

	solve() {
		this.processInstructions()
		this.normalize()
		this.calculateSize()
		return this.size;
	}

	processInstructions() {
		this.instructions.forEach((instruction) => {
			const start = {...this.pos};
			const delta = this.getDeltaFromInstruction(instruction);
			this.pos.x += delta.x;
			this.pos.y += delta.y;
			const end = {...this.pos}
			this.lines[instruction.direction].push({start: start, end: end});
			this.updateCoordinates([start, end])
		});
	}

	normalize() {
		// Also add 1 to x to make sure that row 0 is not in the lagoon
		for (const dir of DIRECTIONS) {
			for (const line of this.lines[dir]) {
				for (const vec of [line.start, line.end]) {
					vec.x += (-this.min.x + 1)
					vec.y += (-this.min.y)
				}
			}
		}
	}

	calculateSize() {
		for (let y = 0; y < this.max.y - this.min.y; y++) {
			const flipPoints = this.getFlipPoints(y);
			
			for (let i = 0; i < flipPoints.length / 2; i++) {
				this.size += (flipPoints[2*i + 1] - flipPoints[2*i] + 1);
			}
		}
	}

	getFlipPoints(y) {
		const flipPoints = new Set();

		for (const dir of DIRECTIONS) {
			for (const line of this.lines[dir]) {
				if (dir === "L" || dir === "R") {
					if (line.start.y === y) {
						flipPoints.add(line.start.x)
						flipPoints.add(line.end.x);
					}
				}
				else if (dir === "U") {
					if (line.start.y <= y && y <= line.end.y) {
						flipPoints.add(line.start.x)
					}
				}
				else if (dir === "D") {
					if (line.end.y <= y && y <= line.start.y) {
						flipPoints.add(line.start.x)
					}
				}
			}
		}

		return sort(Array.from(flipPoints));
	}
}

function part1() {
	return new LagoonMap(smallLagoonInstructions).solve();
}

function part2() {
	// return new LagoonMap(largeLagoonInstructions).solve();
}

function main() {
	console.log(`Part 1: ${part1()}`);
	console.log(`Part 2: ${part2()}`);
}

main();

/* Notes:

...........#######....
...........#.....#....
...........###...#....
.............#...#....
.............#...#....
...........###.###....
...........#...#......
...........##..###.... => This added only 5, because
............#....#....
............######.... => Used a set here because the corners are in two lines

*/
