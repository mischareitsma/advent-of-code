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

const grid = Grid2D.from_lines(lines);
grid.print();

const map = new Grid2D(grid.width, grid.height);

const upExitPipes = ["|", "L", "J"];
const rightExitPipes = ["-", "L", "F"];
const downExitPipes = ["|", "7", "F"];
const leftExitPipes = ["-", "7", "J"];
const allPipes = ["|", "-", "L", "J", "7", "F"];

const pipes = {};
allPipes.forEach(pipe => {
	pipes[pipe] = {
		hasUpExit: upExitPipes.includes(pipe),
		hasRightExit: rightExitPipes.includes(pipe),
		hasDownExit: downExitPipes.includes(pipe),
		hasLeftExit: leftExitPipes.includes(pipe)
	}
});

pipes["."] = {hasUpExit: false, hasRightExit: false, hasDownExit: false, hasLeftExit: false}

const [sx, sy] = grid.getCoords(grid.values.indexOf("S"));
const startPipe = deduceStartPipe();
grid.setValue(sx, sy, startPipe);

const path = {
	currentPipe: startPipe,
	currentX: sx,
	currentY: sy,
	previousDirection: "",
	steps: 0
}

map.setValue(sx, sy, "P");

let reachedStart = false;

const UP = "UP";
const RIGHT = "RIGHT";
const DOWN = "DOWN";
const LEFT = "LEFT";

console.log(JSON.stringify(path));

const route = [];

while (!reachedStart) {
	const routeNode = {
		x: path.currentX,
		y: path.currentY,
		prevNodeDir: path.previousDirection,
		pipe: path.currentPipe,
		dir: undefined,
		step: path.steps
	}
	if ((path.previousDirection !== DOWN) && pipes[path.currentPipe].hasUpExit) {
		path.currentY++;
		path.currentPipe = grid.getValue(path.currentX, path.currentY);
		path.previousDirection = UP;
		routeNode.dir = UP
	}
	else if ((path.previousDirection !== LEFT) && pipes[path.currentPipe].hasRightExit) {
		path.currentX++;
		path.currentPipe = grid.getValue(path.currentX, path.currentY);
		path.previousDirection = RIGHT;
		routeNode.dir = RIGHT
	}
	else if ((path.previousDirection !== UP) && pipes[path.currentPipe].hasDownExit) {
		path.currentY--;
		path.currentPipe = grid.getValue(path.currentX, path.currentY);
		path.previousDirection = DOWN;
		routeNode.dir = DOWN
	}
	else if ((path.previousDirection !== RIGHT) && pipes[path.currentPipe].hasLeftExit) {
		path.currentX--;
		path.currentPipe = grid.getValue(path.currentX, path.currentY)
		path.previousDirection = LEFT
		routeNode.dir = LEFT
	}
	else {
		throw new Error("No more steps to take?");
	}
	path.steps++;
	map.setValue(path.currentX, path.currentY, "P");
	reachedStart = (path.currentX === sx) && (path.currentY === sy);
	route.push(routeNode);
}

for (let i = 0; i < map.values.length; i++) {
	if (map.values[i] !== "P") map.values[i] = ".";
}


function deduceStartPipe() {
	const canGoUp = grid.validY(sy + 1) && pipes[grid.getValue(sx, sy + 1)].hasDownExit
	const canGoRight = grid.validX(sx + 1) && pipes[grid.getValue(sx + 1, sy)].hasLeftExit
	const canGoDown = grid.validY(sy - 1) &&  pipes[grid.getValue(sx, sy - 1)].hasUpExit
	const canGoLeft = grid.validX(sx - 1) && pipes[grid.getValue(sx - 1, sy)].hasRightExit

	for (const pipe in pipes) {
		const exits = pipes[pipe];
		if (
			(canGoUp === exits.hasUpExit) &&
			(canGoRight === exits.hasRightExit) &&
			(canGoDown === exits.hasDownExit) &&
			(canGoLeft === exits.hasLeftExit)
		) return pipe;
	}

	throw new Error("Could not deduce start pipe");
}


function part1() {
	return path.steps / 2;
}

function part2() {
	// TODO: The solution is almost okay, answer is between 560 and 569. There are 9
	// nodes still a ".". The issue is that the direction you can from is not enough, it
	// also depends on the shape of the pipe.

	// Just choose a side, if incorrect, we choose the other side.
	const flipSides = true;

	route.forEach(node => {
		const currentInside = getInsideDirection(node.dir, flipSides);
		let x = node.x;
		let y = node.y;
		switch (currentInside) {
			case LEFT:
				x--;
				break;
			case RIGHT:
				x++;
				break;
			case UP:
				y++;
				break;
			case DOWN:
				y--;
				break;
		}
		if (!map.validCoords(x, y)) return;
		if (map.getValue(x, y) === "P") return;
		map.setValue(x, y, "I");
	});

	route.forEach(node => {
		const currentInside = getInsideDirection(node.dir, !flipSides);
		let x = node.x;
		let y = node.y;
		switch (currentInside) {
			case LEFT:
				x--;
				break;
			case RIGHT:
				x++;
				break;
			case UP:
				y++;
				break;
			case DOWN:
				y--;
				break;
		}
		if (!map.validCoords(x, y)) return;
		if (map.getValue(x, y) === "P") return;
		map.setValue(x, y, "O");
	});


	// All neighbors of I's should be I's as well
	for (let x = 0; x < map.width; x++) {
		for (let y = 0; y < map.height; y++) {
			if (map.getValue(x, y) === "I") {
				flood(map, [x, y], "I");
			}
			if (map.getValue(x, y) === "O") {
				flood(map, [x, y], "O");
			}
		}
	}

	for (let x = 0; x < map.width; x++) {
		for (let y = 0; y < map.height; y++) {
			if (map.getValue(x, y) === "P") {
				map.setValue(x, y, grid.getValue(x, y));
			}
		}
	}
	map.setValue(sx, sy, "S");
	
	map.print()
	console.log(map.values.filter(v=>v===".").length)
	return map.values.filter(v => v==="I").length;
}

function getInsideDirection(dir, flipSides) {
	switch (dir) {
		case UP:
			return flipSides ? LEFT : RIGHT;
		case RIGHT:
			return flipSides ? UP : DOWN;
		case DOWN:
			return flipSides ? RIGHT : LEFT;
		case LEFT:
			return flipSides ? DOWN : UP;
		default:
			throw new Error("Invalid direction " + dir);
	}
}

function flood(map, start, floodVal="F") {

	const floodStack = [];

	floodStack.push(start)
	console.log("Start flood coords: " + start.toString())
	console.log("Start flood value: " + map.getValue(start[0], start[1]))
	const deltas = [1, -1];

	while (floodStack.length) {
		const [x, y] = floodStack.pop();
		console.log(`Flooding ${x}, ${y}`);
		if (map.getValue(x, y) === "P")  continue;

		map.setValue(x, y, floodVal);
		for (const dx of deltas) {
			if (!map.validCoords(x + dx, y)) continue;
			if (map.getValue(x + dx, y) === floodVal) continue;
			floodStack.push([x + dx, y]);
		}
		for (const dy of deltas) {
			if (!map.validCoords(x, y + dy)) continue;
			if (map.getValue(x, y + dy) === floodVal) continue;
			floodStack.push([x, y + dy]);
		}
	}
}

function main() {
	console.log(`Part 1: ${part1()}`);
	console.log(`Part 2: ${part2()}`);
}

main();
