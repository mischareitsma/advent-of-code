import { readFileSync } from "node:fs";
import { dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { sort } from "../math.js";

const __dirname = dirname(fileURLToPath(import.meta.url));

const isTest = false;
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

	isHorizontal(fp) {
		return fp.dir === "R" || fp.dir === "L";
	}

	isOtherDir(fp1, fp2) {
		// Bit under the assumption this is always called with U/D points only, as R !== U
		return fp1.dir !== fp2.dir;
	}

	calculateSizeV2() {
		for (let y = 0; y < this.max.y - this.min.y + 1; y++) {
			if (y % 1000000 === 0)
				console.log(y);

			this.size += this.getFlipPointsV2().getSize();
		}
	}

	calculateSize() {


		for (let y = 0; y < this.max.y - this.min.y + 1; y++) {
			if (y % 1000000 === 0)
				console.log(y);
			const flipPoints = this.getFlipPoints(y);

			let i = 0;

			if (y === 34)
				console.log("hack");

			let prev_i = -1;
			while (i < flipPoints.length - 1) {

				if (prev_i === i) {
					throw new Error("Error issues");
				}
				prev_i = i;

				const startPoint = flipPoints[i++]

				let nextPoint = flipPoints[i++];
				let nextPoint2 = flipPoints[i+1];

				if (this.isHorizontal(nextPoint)) {
					nextPoint = flipPoints[i++];
				}
				else if (nextPoint2 && this.isHorizontal(nextPoint2)) {
					// So we got a situation like D UL => D is the "Start"
					i--;
				}
				else {
					this.size += (nextPoint.max - startPoint.min + 1);
					continue;
				}

				
				if (this.isOtherDir(startPoint, nextPoint)) {
					this.size += (nextPoint.max - startPoint.min + 1);
					continue;
				}

				// If we get here, we have something like ULU or DRD or something, so just the starting boundary.

				let max = 0;

				while (max === 0) {
					let nextPoint = flipPoints[i++];
					let nextPoint2 = flipPoints[i];

					if (!nextPoint2 || !this.isHorizontal(nextPoint2)) {
						max = nextPoint.max;
						break;
					}

					let nextPoint3 = flipPoints[i+1];
					i+=2;

					if (this.isOtherDir(nextPoint, nextPoint3)) {
						continue;
					}

					max = nextPoint3.max;
				}

				this.size += (max - startPoint.min + 1);
			}
		}
	}

	getFlipPointsV2(y) {
		const flipPoints = new FlipPoints(y)
		for (const dir of DIRECTIONS) {
			for (const line of this.lines[dir]) {
				flipPoints.add(line);
			}
		}
		flipPoints.process()
	}

	getFlipPoints(y) {
		const flipPoints = [];
		for (const dir of DIRECTIONS) {
			// TODO: Store type (hor, vert, and s/e (where for v, s===e))
			for (const line of this.lines[dir]) {
				
				if (dir === "L" || dir === "R") {
					if (line.start.y === y) {
						const min = Math.min(line.start.x, line.end.x);
						const max = Math.max(line.start.x, line.end.x);
						flipPoints.push({
							dir: dir,
							min: min,
							max: max
						});
					}
				}
				else if (dir === "U") {
					if (line.start.y <= y && y <= line.end.y) {
						flipPoints.push({
							dir: dir,
							min: line.start.x,
							max: line.start.x
						});
					}
				}
				else if (dir === "D") {
					if (line.end.y <= y && y <= line.start.y) {
						flipPoints.push({
							dir: dir,
							min: line.start.x,
							max: line.start.x
						});
					}
				}
			}
		}

		flipPoints.sort((a, b) => {
			if (a.min === a.max && a.min === b.min) return -1;
			if (a.min === a.max && a.max === b.min) return 1;
			return a.min - b.min
		});
		return flipPoints
	}
}

class FlipPoints {
	lineInfo = [];
	flipPoints = [];

	
	constructor(y) {
		this.y = y;
	}

	add(line) {
		const isHorizontal = line.dir === "R" || line.dir === "L";
		const isVertical = !isHorizontal;

		if (isHorizontal && line.start.y !== this.y)
			return;
		
		const yMin = Math.min(line.start.y, line.end.y);
		const yMax = Math.max(line.start.y, line.end.y);

		if (y < yMin || y > yMax)
			return;

		const xMin = Math.min(line.start.x, line.end.x);
		const xMax = Math.max(line.start.x, line.end.x);
	
		this.lineInfo.push({
			start: start,
			end: end,
			min: xMin,
			max: xMax,
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
		while (i < this.lineInfo.length - 1) {
			const currentLine = nextLine ? nextLine : this.lineInfo[i++];
			nextLine = this.lineInfo[i++];

			if (nextLine && nextLine.isVertical) {
				this.flipPoints.push({
					type: "V",
					subType: "",
					min: currentLine.min,
					max: currentLine.max,
				});
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

	getSize() {

	}

	
}



function part1() {
	return new LagoonMap(smallLagoonInstructions).solve();
}

function part2() {
	return new LagoonMap(largeLagoonInstructions).solve();
}

function main() {
	console.log(`Part 1: ${part1()} (test: 62)`);
	console.log(`Part 2: ${part2()} (test: 952408144115, 67622704086408 too low)`);
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
