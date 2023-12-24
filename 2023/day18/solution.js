import { readFileSync } from "node:fs";
import { dirname } from "node:path";
import { fileURLToPath } from "node:url";

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
		for (let y = 0; y < this.max.y - this.min.y + 1; y++) {
			this.size += this.getFlipPoints(y).getSize();
		}
	}

	getFlipPoints(y) {
		const flipPoints = new FlipPoints(y)
		for (const dir of DIRECTIONS) {
			for (const line of this.lines[dir]) {
				flipPoints.add({...line, dir:dir});
			}
		}
		flipPoints.process()
		return flipPoints;
	}
}

class FlipPoints {
	lineInfo = [];
	flipPoints = [];

	constructor(y) {
		this.y = y;
	}
	// TODO: (Mischa Reitsma) Add could take care of getting it in a correct y-bucket, takes more memory, but only loop through all lines once
	add(line) {
		const isHorizontal = (line.start.y === line.end.y);
		const isVertical = (line.start.x === line.end.x);

		if (isHorizontal && line.start.y !== this.y)
			return;
		
		const yMin = Math.min(line.start.y, line.end.y);
		const yMax = Math.max(line.start.y, line.end.y);

		if (this.y < yMin || this.y > yMax)
			return;

		const xMin = Math.min(line.start.x, line.end.x);
		const xMax = Math.max(line.start.x, line.end.x);
	
		this.lineInfo.push({
			start: line.start,
			end: line.end,
			min: xMin,
			max: xMax,
			dir: line.dir,
			isHorizontal: isHorizontal,
			isVertical: isVertical
		})
	}

	_sort() {
		this.lineInfo.sort((a, b) => {
			if (a.min === a.max && a.min === b.min) return -1;
			if (a.min === a.max && a.max === b.min) return 1;
			return a.min - b.min
		});
	}

	process() {
		this._sort();

		// Transform to points that are either vertical or the four
		// types of horizontal
		let i = 0;
		let nextLine;
		while (i < this.lineInfo.length) {
			const currentLine = nextLine ? nextLine : this.lineInfo[i++];
			nextLine = this.lineInfo[i++];

			if (nextLine && nextLine.isVertical) {
				this.flipPoints.push({
					type: "V",
					subType: "",
					min: currentLine.min,
					max: currentLine.max,
				});
				i--;
				nextLine = null;
				continue;
			}

			if (!nextLine) {
				if (!currentLine.isVertical) throw new Error("This is weird")
				// currentLine is last one in the array
				this.flipPoints.push({
					type: "V",
					subType: "",
					min: currentLine.min,
					max: currentLine.max,
				})
				continue;
			}

			// If we get here, nextLine exists and is horizontal.
			const lastLine = this.lineInfo[i++];

			this.flipPoints.push({
				type: "h",
				subType: `${currentLine.dir}${lastLine.dir}`,
				min: currentLine.min,
				max: lastLine.max
			});

			nextLine = null;
		}
	}

	isUTurn(fp) {
		return fp.subType === "UD" || fp.subType === "DU";
	}

	getSize() {
		let adding = false;
		let size = 0;
		let min = 0;

		this.flipPoints.forEach((fp) => {
			if (!adding) {
				if (this.isUTurn(fp)) {
					size += fp.max - fp.min + 1;
					return;
				}
				adding = true;
				min = fp.min
			}
			else {
				if (this.isUTurn(fp)) return;
				adding = false;
				size += fp.max - min + 1;
			}
		});
		return size;
	}
}

function part1() {
	return new LagoonMap(smallLagoonInstructions).solve();
}

function part2() {
	return new LagoonMap(largeLagoonInstructions).solve();
}

function main() {
	const answerPart1 = part1();
	const testPart1 = 62
	console.log(`Part 1: ${answerPart1} (test${!isTest ? "" : testPart1 === answerPart1 ? " OK" : " NOK"}: ${testPart1})`);

	const answerPart2 = part2();
	const testPart2 = 952408144115;
	console.log(`Part 2: ${answerPart2} (test${!isTest ? "" : testPart2 === answerPart2 ? " OK" : " NOK"}: ${testPart2})`);
}

main();
