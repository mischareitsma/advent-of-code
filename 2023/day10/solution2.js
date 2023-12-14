import * as fs from "node:fs";
import { dirname } from "path";
import { fileURLToPath } from "url";
import { Grid2D } from "../map.js";

const __dirname = dirname(fileURLToPath(import.meta.url));

const isTest = false;
const testNumber = 3;

const fname = (isTest ? `test${testNumber}_` : "") + "input.dat";

const lines = fs.readFileSync(__dirname + "/" + fname).toString().split("\n");
lines.pop();

const tempGrid = Grid2D.from_lines(lines);

// Grow grid with size 1, doesn't affect the path, but makes figuring out what is in and outside
// the loop easier.
const grid = new Grid2D(tempGrid.width + 2, tempGrid.height + 2);
for (let x = 0; x < tempGrid.width; x++) {
	for (let y = 0; y < tempGrid.height; y++) {
		grid.setValue(x+1, y+1, tempGrid.getValue(x, y));
	}
}

function getStart(g) {
	const [sx, sy] = g.getCoords(grid.values.indexOf("S"));
	return {x: sx, y: sy};
}

const start = getStart(grid);

const pipes = {
	horizontal: {
		value: "-",
		up: false,
		right: true,
		down: false,
		left: true,
	},
	vertical: {
		value: "|",
		up: true,
		right: false,
		down: true,
		left: false,
	},
	downRight: {
		value: "F",
		up: false,
		right: true,
		down: true,
		left: false,
	},
	downLeft: {
		value: "7",
		up: false,
		right: false,
		down: true,
		left: true,
	},
	upRight: {
		value: "L",
		up: true,
		right: true,
		down: false,
		left: false,
	},
	upLeft: {
		value: "J",
		up: true,
		right: false,
		down: false,
		left: true,
	},
};

const sides = {
	up: "up",
	right: "right",
	down: "down",
	left: "left"
};

const tiles = {
	point: {
		value: ".",
		up: false,
		right: false,
		down: false,
		left: false,
	},
	...pipes
};

const valueToTile = {}
for (const tile in tiles) {
	valueToTile[tiles[tile].value] = tiles[tile]
}

const routeMap = new Grid2D(grid.width, grid.height, tiles.point);

function deduceStartTile() {
	const canGoUp = grid.validY(start.y + 1) &&
		valueToTile[grid.getValue(start.x, start.y + 1)].down;

	const canGoRight = grid.validX(start.x + 1) &&
		valueToTile[grid.getValue(start.x + 1, start.y)].left;

	const canGoDown = grid.validY(start.y - 1) &&
		valueToTile[grid.getValue(start.x, start.y - 1)].up;

	const canGoLeft = grid.validX(start.x - 1) &&
		valueToTile[grid.getValue(start.x - 1, start.y)].right;

	for (const tile in tiles) {
		if (
			(canGoUp === tiles[tile].up) &&
			(canGoRight === tiles[tile].right) &&
			(canGoDown === tiles[tile].down) &&
			(canGoLeft === tiles[tile].left)
		) return valueToTile[tiles[tile].value];
	}

	throw new Error("Could not deduce start tile");
}

// Deduce the start pipe and replace:
const startTile = deduceStartTile();

function createRoute() {

}

const startRoute = {
	tile: startTile,
	position: start,
	sideOne: [],
	sideTwo: [],
	forward: "",
	backward: "",
}
