import * as fs from "node:fs";
import { dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));

const isTest = true;
const testNumber = 1;

const fname = (isTest ? `test${testNumber}_` : "") + "input.dat";

const lines = fs.readFileSync(__dirname + "/" + fname).toString().split("\n");
lines.pop();

const map = [];

for (let i = 0; i < lines.length; i++) {
	map.push(Array.from(lines[lines.length - i - 1]));
}

// const map = lines.map(line => Array.from(line));

// TODO: Move a prefilled creation of an NxM matrix to utils.
const rows = lines.length;
const columns = lines[0].length;

const visited = [];
let r = rows;
while (r--) {
	const values = []
	let c = columns;
	while (c--) values.push(false);
	visited.push(values)
}

function getStart() {
	for (let y = 0; y < map.length; y++) {
		for (let x = 0; x < map[y].length; x++) {
			if (map[y][x] === "S") return [x, y];
		}
	}
}
print_map();
const [sx, sy] = getStart();
// visited[sy][sx] = true;

function getLoopLength() {
	let prev_x = sx;
	let prev_y = sy;
	let [x, y] = getStartStep();

	let length = 0;
	let completed = false

	visited[sy][sx] = true;

	while (!completed) {
		length++;
		visited[y][x] = true;
		print_map();
		const [new_x, new_y] = getNextStep(x, y, prev_x, prev_y);
		prev_x = x;
		prev_y = y;
		x = new_x;
		y = new_y;
		completed = (x === sx) && (y === sy);
	}

	return length;
}

function print_map() {
	map.forEach((row, y) => {
		row.forEach((column, x) => {
		if (visited[y][x])
			process.stdout.write(`\x1b[31m${column}\x1b[0m`);
		else
			process.stdout.write(column);
		});
		process.stdout.write("\n");
	});
	console.log("--------------");

}


const canGoLeft = ["-", "7", "J"];
const canGoRight = ["-", "F", "L"];
const canGoUp = ["|", "L", "J"];
const canGoDown = ["|", "F", "7"];

function getNextStep(x, y, px, py) {
	const currentPipe = map[y][x];

	const cameFromLeft = (px < x);
	const cameFromRight = (px > x);
	const cameFromDown = (py < y);
	const cameFromUp = (py > y);
	
	if ((x - 1 >= 0) && canGoLeft.includes(currentPipe) && !cameFromLeft) {
		if (canGoRight.includes(map[y][x-1]) && (px !== x-1)) return [x-1, y];
	}
	if ((x + 1 < columns) && canGoRight.includes(currentPipe) && !cameFromRight) {
		if (canGoLeft.includes(map[y][x+1]) && (px !== x+1)) return [x+1, y];
	}
	if ((y + 1 < rows) && canGoUp.includes(currentPipe) && !cameFromUp) {
		if (canGoDown.includes(map[y+1][x]) && (py !== y+1)) return [x, y+1];
	}
	if ((y - 1 >= 0) && canGoDown.includes(currentPipe) && !cameFromDown) {
		if (canGoUp.includes(map[y-1][x]) && (py !== y-1)) return [x, y-1];
	}

	throw new Error("No new route found?");
}

function getStartStep() {
	// TODO: Ugly, could do somthing like {dir: {x: 0, y: 1}, canMove: canGoUp} and than double loop that
	// Just pretend that outside map are dots, could also make the map bigger to not have these
	// edge cases, as then those nodes are never reachable.
	const up = (sy + 1 < rows) ? map[sy + 1][sx] : ".";
	const down = (sy - 1 >= 0) ? map[sy - 1][sx] : ".";
	const left = (sx - 1 >= 0) ? map[sy][sx - 1] : ".";
	const right = (sx + 1 < columns) ? map[sy][sx + 1] : ".";

	if (canGoUp.includes(up)) {
		if (
			canGoLeft.includes(left) ||
			canGoRight.includes(right) ||
			canGoDown.includes(down)
		) return [sx, sy + 1];
	}
	if (canGoDown.includes(down)) {
		if (
			canGoLeft.includes(left) ||
			canGoRight.includes(right) ||
			canGoUp.includes(up)
		) return [sx, sy - 1];
	}
	if (canGoRight.includes(right)) {
		if (
			canGoLeft.includes(left) ||
			canGoUp.includes(up) ||
			canGoDown.includes(down)
		) return [sx + 1, sy];
	}
	if (canGoLeft.includes(left)) {
		if (
			canGoRight.includes(right) ||
			canGoUp.includes(up) ||
			canGoDown.includes(down)
		) return [sx - 1, sy];
	}

	throw new Error("Could not find start direction");
}

function part1() {
	return getLoopLength() / 2;
}

function part2() {
	return "";
}

function main() {
	console.log(`Part 1: ${part1()}`);
	console.log(`Part 2: ${part2()}`);
}

main();
