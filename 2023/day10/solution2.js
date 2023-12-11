import * as fs from "node:fs";
import { dirname } from "path";
import { fileURLToPath } from "url";
import { Grid2D } from "./map.js";

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
	horizontal: "-",
	vertical: "|",
	downRight: "F",
	downLeft: "7",
	upRight: "L",
	upLeft: "J"
};

const tiles = {
	point: ".",
	...pipes
};

const routeMap = new Grid2D(grid.width, grid.height, tiles.point);
