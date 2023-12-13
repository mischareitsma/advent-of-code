import * as fs from "node:fs";
import { dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));

const isTest = false;
const testNumber = "";

const fname = (isTest ? `test${testNumber}_` : "") + "input.dat";

const lines = fs.readFileSync(__dirname + "/" + fname).toString().split("\n");
lines.pop();

const maps = [];
let currentMap = [];
lines.push("");
lines.forEach(line => {
	if (line === "") {
		const rotatedMap = getRotatedMap(currentMap);
		maps.push({
			map: currentMap,
			horizontalReflection: getReflectionPoint(currentMap),
			verticalReflection: getReflectionPoint(rotatedMap),
			horizontalWithFix: getReflectionWithFix(currentMap),
			verticalWithFix: getReflectionWithFix(rotatedMap),
		});
		currentMap = [];
	}
	else {
		currentMap.push(line);
	}
});

function getRotatedMap(map) {
	const w = map[0].length;
	const h = map.length;
	const rotatedMap = [];
	for (let j = 0; j < w; j++) {
		const row = [];
		for (let i = 0; i < h; i++) {
			row.push(map[h-1-i][j]);
		}
		rotatedMap.push(row.join(""));
	}
	return rotatedMap;
}

function getReflectionPoint(map) {
	const possibleReflectionColumns = [];
	for (let i = 0; i < map.length - 1; i++) {
		if (map[i] === map[i+1])
			possibleReflectionColumns.push(i);
	}

	while (possibleReflectionColumns.length) {
		const rp = possibleReflectionColumns.pop();

		let isReflection = true;
		for (let i=rp, j=rp+1; i >= 0 && j < map.length && isReflection; i--, j++) {
			isReflection = (map[i] === map[j]);
		}
		
		if (isReflection)
			return rp + 1;
	}

	return 0;
}

function getReflectionWithFix(map) {
	const possibleReflectionPoints = [];
	for (let i = 0; i < map.length - 1; i++) {
		if (difference(map[i], map[i+1]) < 2)
			possibleReflectionPoints.push(i);
	}

	while (possibleReflectionPoints.length) {
		const rp = possibleReflectionPoints.pop()
		let smudgeFixed = false
		let isReflection = true;

		for (let i=rp, j=rp+1; i >= 0 && j < map.length && isReflection; i--, j++) {
			const diff = difference(map[i], map[j]);
			if (diff > 1)
				isReflection = false;
			if (diff === 1) {
				if (smudgeFixed)
					isReflection = false;
				else
					smudgeFixed = true;
			}
		}

		if (isReflection && smudgeFixed)
			return rp + 1;
	}

	return 0;
}

function difference(line1, line2) {
	// Skip some of the safety checks like length, we know lengths are equal
	let difference = 0;

	for (let i = 0; i < line1.length; i++) {
		if (line1[i] !== line2[i])
			difference++;
	}

	return difference;

}

function part1() {
	let result = 0;
	maps.forEach(m => {
		result += ((m.verticalReflection) + 100 * (m.horizontalReflection));
	});
	return result;
}

function part2() {
	let result = 0;
	maps.forEach(m => {
		result += ((m.verticalWithFix) + 100 * (m.horizontalWithFix));
	});
	return result;
}

function main() {
	console.log(`Part 1: ${part1()}`);
	console.log(`Part 2: ${part2()}`);
}

main();
