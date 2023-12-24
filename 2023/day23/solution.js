import { readFileSync } from "node:fs";
import { dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { Grid2D } from "../map.js";

const __dirname = dirname(fileURLToPath(import.meta.url));

const isTest = true;
const testNumber = "";

const fname = (isTest ? `test${testNumber}_` : "") + "input.dat";

const lines = readFileSync(__dirname + "/" + fname).toString().split("\n");
lines.pop();

const initialMap = Grid2D.from_lines(lines);

const TILES = {
	rock: "#",
	path: ".",
	upSlope: "^",
	leftSlope: "<",
	rightSlope: ">",
	downSlope: "v",
}

const map = new Grid2D(initialMap.width, initialMap.height);

const start = { x: 1, y: initialMap.height - 1, idx: initialMap.getIndex(1, initialMap.height - 1) }
const end = {x: initialMap.width - 2, y: 0, idx: initialMap.getIndex(initialMap.width - 2, 0) }

initialMap.values.forEach((value, idx) => {
	const [x, y] = initialMap.getCoords(idx);
	map.setValue(x, y, {
		x: x, y: y, idx: idx, tile: value, directions: [], isStart: false, isEnd: false,
		isPath: value !== TILES.rock, allDirections: [],
		edgeIndices: null, nodes: null
	})
});

map.values[start.idx].isStart = true;
map.values[end.idx].isEnd = true;

const ALL_DELTAS = {
	up: {dx:0, dy: 1},
	left: {dx: -1, dy: 0},
	right: {dx: 1, dy: 0},
	down: {dx: 0, dy: -1}
};

const DELTAS = {
	".": [ALL_DELTAS.up, ALL_DELTAS.left, ALL_DELTAS.right, ALL_DELTAS.down],
	"^": [ALL_DELTAS.up],
	"<": [ALL_DELTAS.left],
	">": [ALL_DELTAS.right],
	"v": [ALL_DELTAS.down]
}

function isReachable(tile, dx, dy) {
	if (tile === ".") return true;
	if (tile === "^" && dy !== -1) return true;
	if (tile === "<" && dx !== 1) return true;
	if (tile === ">" && dx !== -1) return true;
	if (tile === "v" && dy !== 1) return true;

	return false;
}

map.values.filter(v => v.isPath).forEach(pathInfo => {
	DELTAS[pathInfo.tile].forEach(delta => {
		const nx = pathInfo.x + delta.dx;
		const ny = pathInfo.y + delta.dy;

		if (!map.validCoords(nx, ny))
			return;

		const otherTile = map.getValue(nx, ny);

		if (!otherTile.isPath)
			return;

		if (!isReachable(otherTile.tile, delta.dx, delta.dy))
			return;

		pathInfo.directions.push(map.getIndex(nx, ny));
	});
	DELTAS["."].forEach(delta => {
		const nx = pathInfo.x + delta.dx;
		const ny = pathInfo.y + delta.dy;

		if (!map.validCoords(nx, ny))
			return;

		if (!map.getValue(nx, ny).isPath)
			return;

		pathInfo.allDirections.push(map.getIndex(nx, ny));
	});
});

map.values.filter(v => v.allDirections.length === 2).forEach((pathInfo) => {
	// Already processed this edge
	if (pathInfo.edgeIndices) return;

	const edgeIndices = [pathInfo.idx];
	const nodes = [];
	pathInfo.edgeIndices = edgeIndices;
	pathInfo.nodes = nodes;

	for (const startIter of pathInfo.allDirections) {
		let currentPath = map.values[startIter];
		let previousPath = pathInfo;

		while (currentPath.allDirections.length === 2) {
			edgeIndices.push(currentPath.idx);
			currentPath.edgeIndices = edgeIndices;
			currentPath.nodes = nodes;
			const newPathIdx = currentPath.allDirections.filter(idx => idx !== previousPath.idx)[0];
			previousPath = currentPath;
			currentPath = map.values[newPathIdx];
		}

		nodes.push(currentPath.idx);
	}
});

function getLongestPathLength(ignoreSlopes) {
	const graphPaths = [{nodes: [start.idx], length: 0}];

	let maxPathLength = 0;
	
	while (graphPaths.length) {
		const currentPath = graphPaths.pop();
		const lastStep = currentPath.nodes.at(-1);
	
		if (lastStep === end.idx) {
			maxPathLength = Math.max(maxPathLength, currentPath.length);
			continue;
		}
	
		const lastTile = map.values[lastStep];
	
		const newNodes = [];
	
		const directions = ignoreSlopes ? lastTile.allDirections : lastTile.directions

		directions.forEach((idx) => {
			const edgeTile = map.values[idx];
			const nextNode = edgeTile.nodes.filter(v => v !== lastStep)[0];
			if (!currentPath.nodes.includes(nextNode))
				newNodes.push({node: nextNode, length: edgeTile.edgeIndices.length});
		});
	
		newNodes.forEach(edgeInfo => {
			const newPath = {
				nodes: [...currentPath.nodes],
				length: currentPath.length
			};
			newPath.nodes.push(edgeInfo.node);
			newPath.length += edgeInfo.length + 1
			graphPaths.push(newPath)
		});
	}

	return maxPathLength;
}

function part1() {
	return getLongestPathLength(false);
}

function part2() {
	return getLongestPathLength(true);
}

function main() {
	const answerPart1 = part1();
	const testPart1 = 94
	console.log(`Part 1: ${answerPart1} (test${!isTest ? "" : testPart1 === answerPart1 ? " OK" : " NOK"}: ${testPart1})`);

	const answerPart2 = part2();
	const testPart2 = 154;
	console.log(`Part 2: ${answerPart2} (test${!isTest ? "" : testPart2 === answerPart2 ? " OK" : " NOK"}: ${testPart2})`);
}

main();
