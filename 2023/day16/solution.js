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

const tiles = Grid2D.from_lines(lines);

function getNewVisitedMap() {
	const visitedMap = new Grid2D(tiles.width, tiles.height);
	for (let x = 0; x < visitedMap.width; x++) {
		for (let y = 0; y < visitedMap.height; y++) {
			visitedMap.setValue(x, y, {
				up: false,
				left: false,
				right: false,
				down: false,
				nDirections: 0
			});
		}
	}
	return visitedMap;
}

const pathMap = new Grid2D(tiles.width, tiles.height);
for (let x = 0; x < pathMap.width; x++) {
	for (let y = 0; y < pathMap.height; y++) {
		pathMap.setValue(x, y, {
			mapped: false,
			up: [],
			left: [],
			right: [],
			down: []
		});
	}
}

const TILE = {
	mirrorDown: "\\",
	mirrorUp: "/",
	splitterHorizontal: "-",
	splitterVertical: "|",
	empty: "."
}

const TRANSFORMED_DIRECTIONS = {
	"\\": {
		up: ["left"],
		left: ["up"],
		right: ["down"],
		down: ["right"],
	},
	"/": {
		up: ["right"],
		left: ["down"],
		right: ["up"],
		down: ["left"]
	},
	"-": {
		up: ["left", "right"],
		left: ["left"],
		right: ["right"],
		down: ["left", "right"]
	},
	"|": {
		up: ["up"],
		left: ["up", "down"],
		right: ["up", "down"],
		down: ["down"]
	},
	".": {
		up: ["up"],
		left: ["left"],
		right: ["right"],
		down: ["down"]
	}
}

const DIRECTION = {
	up: {x: 0, y: 1},
	left: {x: -1, y: 0},
	right: {x: 1, y: 0},
	down: {x: 0, y: -1}
}

function addAllCombos(x, y, tile) {
	const pm = pathMap.getValue(x, y)
	for (const dir in DIRECTION) {
		for (const newDir of TRANSFORMED_DIRECTIONS[tile][dir]) {
			const p = {x: x, y: y};
			p.x += DIRECTION[newDir].x;
			p.y += DIRECTION[newDir].y;

			if (pathMap.validCoords(p.x, p.y))
					pm[dir].push({x: p.x, y: p.y, dir: newDir});
		}
	}
	pm.mapped = true;
}

for (let x = 0; x < tiles.width; x++) {
	for (let y = 0; y < tiles.height; y++) {
		addAllCombos(x, y, tiles.getValue(x, y));
	}
}

const energizedValues = [];

for (let x = 0; x < pathMap.width; x++) {
	energizedValues.push({x: x, y: 0, direction: "up", value: 0});
	energizedValues.push({x: x, y: pathMap.height - 1, direction: "down", value: 0});
}

for (let y = 0; y < pathMap.width; y++) {
	energizedValues.push({x: 0, y: y, direction: "right", value: 0});
	energizedValues.push({x: pathMap.width - 1, y: y, direction: "left", value: 0});
}

energizedValues.forEach(v => {
	const paths = [{
		x: v.x, y: v.y, dir: v.direction
	}];
	
	const visitedMap = getNewVisitedMap();

	while (paths.length) {
		const path = paths.pop();
		if (visitedMap.getValue(path.x, path.y)[path.dir])
			continue;
		const visitedNode = visitedMap.getValue(path.x, path.y);
		visitedNode.nDirections++;
		visitedNode[path.dir] = true;
		pathMap.getValue(path.x, path.y)[path.dir].forEach(p => {paths.push(p);});
	}

	v.value = visitedMap.values.filter(v => v.nDirections > 0).length;
});

function part1() {
	return energizedValues.filter(v => {
		return v.x === 0 && v.y === pathMap.height - 1 && v.direction === "right"
	})[0].value
}

function part2() {
	return Math.max(...energizedValues.map(v => v.value));
}

function main() {
	console.log(`Part 1: ${part1()}`);
	console.log(`Part 2: ${part2()}`);
}

main();
