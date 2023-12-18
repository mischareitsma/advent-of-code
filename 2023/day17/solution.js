import { readFileSync } from "node:fs";
import { dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { Grid2D } from "../map.js";

const __dirname = dirname(fileURLToPath(import.meta.url));

const isTest = false;
const testNumber = 2;

const fname = (isTest ? `test${testNumber}_` : "") + "input.dat";

const lines = readFileSync(__dirname + "/" + fname).toString().split("\n");
lines.pop();

const cityMap = Grid2D.from_lines(lines, v => Number.parseInt(v));

const DIRECTION = {
	up: {x: 0, y: 1},
	left: {x: -1,y:  0},
	right: {x: 1, y: 0},
	down: {x: 0, y: -1}
}

const TURNS = {
	up: ["left", "right"],
	left: ["up", "down"],
	right: ["up", "down"],
	down: ["left", "right"]
}

class Path {
	constructor(x, y, dir, steps, value) {
		this.x = x;
		this.y = y;
		this.dir = dir;
		this.steps = steps;
		this.value = value;
	}

	/**
	 * 
	 * @returns {Path}
	 */
	copy() {
		return new Path(this.x, this.y, this.dir, this.steps, this.value);
	}

	move() {
		this.x += DIRECTION[this.dir].x;
		this.y += DIRECTION[this.dir].y;
		this.steps++;
	}

	getMovedPath(newDir) {
		const newPath = this.copy();

		if (newDir) {
			newPath.dir = newDir;
			newPath.steps = 0;
		}

		newPath.move();

		if (!cityMap.validCoords(newPath.x, newPath.y))
			return null;

		newPath.value += cityMap.getValue(newPath.x, newPath.y);

		return newPath;
	}

	setKey() {
		return `${this.x},${this.y},${this.dir},${this.steps}`;
	}

	reachedEnd() {
		return (this.x === cityMap.width - 1) && (this.y === 0);
	}

	validReach(minSteps) {
		return (this.steps > minSteps);
	}
}

// Prio-queue-ish? Also do visited here, bit cheaty?
class PathQueue {

	visited = new Set();

	constructor(maxValue) {
		this.maxValue = maxValue;
		this.paths = new Array(this.maxValue);
		for (let i = 0; i < this.maxValue; i++) {
			this.paths[i] = [];
		}
	}

	/**
	 * Add path
	 * 
	 * @param {Path} p path to add
	 */
	push(p) {
		if (!p)
			return;

		if (p.value >= this.maxValue)
			throw new Error(`Value ${p.value} breached ${this.maxValue}`);

		if (this.visited.has(p.setKey()))
			return;

		this.paths[p.value].push(p)
		this.visited.add(p.setKey());
	}

	/**
	 * @returns {Path[]} Array of paths with best prio
	 */
	pop() {
		for (let i = 0; i < this.maxValue; i++) {
			if (this.paths[i].length) {
				const returnArray = this.paths[i];
				this.paths[i] = [];
				return returnArray;
			}
		}

		// TODO: or throw error?
		return [];
	}
}

function solve(minSteps, maxSteps) {
	const q = new PathQueue(5000);
	// const visited = new Set();
	
	q.push(new Path(0, cityMap.height - 1, "right", 0, 0))
	q.push(new Path(0, cityMap.height - 1, "down", 0, 0))

	let currentPaths = q.pop()

	while (currentPaths.length) {
		for (const path of currentPaths) {
			// visited.add(path.setKey());
			const dirs = [];

			if (path.steps < maxSteps) {
				dirs.push(null);
			}

			if (path.steps > minSteps) {
				for (const dir of TURNS[path.dir]) {
					dirs.push(dir)
				}
			}

			for (const d of dirs) {
				const newPath = path.getMovedPath(d);

				if (!newPath)
					continue;

				if (newPath.reachedEnd() && newPath.validReach(minSteps))
					return newPath.value;
				else
					q.push(newPath)


			}
		}
		currentPaths = q.pop()
	}
}

function part1() {
	return solve(0, 3);
}

function part2() {
	return solve(3, 10);
}

function main() {
	console.log(`Part 1: ${part1()}`);
	console.log(`Part 2: ${part2()}`);
}

main();
