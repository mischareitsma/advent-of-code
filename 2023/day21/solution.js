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

const TILES = {
	garden: ".",
	start: "S",
	visited: "O",
	rock: "#"
}

const STEPS = isTest ? 6 : 64; // Steps for part 1

const map = Grid2D.from_lines(lines);

const START = map.getCoords(map.values.indexOf(TILES.start));

const DELTAS = [
	{dx: 0, dy: 1},
	{dx: -1, dy: 0},
	{dx: 1, dy: 0},
	{dx: 0, dy: -1}
];

// Could memoize map values vs steps, start_x, start_y
function getPlotsAfterSteps(map, steps, start_x, start_y) {
	const currentMap = map.copy();
	currentMap.setValue(start_x, start_y, TILES.visited);

	while (steps--) {
		const unsetCoords = [];
		const setCoords = new Set();
		currentMap.values.forEach((steppedOn, idx) => {
			if (steppedOn !== TILES.visited) return;
	
			const [x, y] = currentMap.getCoords(idx);
			unsetCoords.push(idx);
	
			DELTAS.forEach(delta => {
				const xn = x + delta.dx;
				const yn = y + delta.dy;
	
				if (!currentMap.validCoords(xn, yn)) return;
				if (currentMap.getValue(xn, yn) === TILES.rock) return;
	
				setCoords.add(currentMap.getIndex(xn, yn));
			});
		});

		unsetCoords.forEach(idx => currentMap.values[idx] = TILES.garden);
		setCoords.forEach(idx => currentMap.values[idx] = TILES.visited);
	}

	return currentMap.values.filter(v => v === TILES.visited).length;
}

function part1() {
	return getPlotsAfterSteps(map, STEPS, START[0], START[1]);
}

function part2() {
	if (isTest) return "Test grid is a pain, not running part2 with test";

	/* Old code had a lot of analysis stuff. Some learnings:
	- map center has an empty row + column, and empty rows around the rest. So
	  fastest way N, S, E, W is always through the centers, and NE, SE, NW, SE if through center
	  and then along those sides. Which means (size of map is 131) it takes 65 steps to get to
	  the edge from S. then another 131 we can get to the other edge on the next map etc.
	- The number is nice. number - 65 (steps to get to edge of original map) is divisible by 131
	- A map that is fully visited will alternate between two states (odd or even amount of steps
	  on the map).
	- Drew the shapes on a good old notebook, diamond shaped with a lot of full maps. These maps
	  will alternate between the two states. As the total number of steps is odd, it means the
	  original map will be in the state of odd steps, the neighbors the state after an even
	  amount of steps, etc. The N, S, E and W directions we can get the number of plots with
	  as starting position the middle of X or y, and then 0 or 130 for x or y, and then do
	  130 steps. The edges will alternate between to types of states. One starting at any of
	  the four corners and doing 64 more steps (takes 66 steps to get to that corner, and then
	  we are left with 130 - 66 = 64 steps. The other one has 131 steps more (go up for example
	  the last full tile, were the 64 is if we go up in the last tile)
	- The number of tiles can be calculated. It follows a pattern (which was also drawn in my
	  notebook :-)). But tried to tabulate the first few times we do 131 steps below:

	131 steps | full tiles | small corners | big corners
	1         | 1 (0 odd)  | 1             | 0
	2         | 5 (4 even) | 2             | 1
	3         | 13(4 even) | 3             | 2
	4         | 25(16 even)| 4             | 3

	As we have an "even" amount of steps, the pattern there is: N^2 even plots (2^2= 4,4^2=16)
	and an (N-1)^2 uneven plots (2-1)^2 = 1, 4 + 1 = 5, (4-1)^2 = 9, 9+16=25
	*/

	const mapSize = map.width;
	const mapEdge = mapSize - 1
	const center = (mapSize - 1) / 2
	const totalSteps = 26501365;
	const totalTiles = (totalSteps - center) / mapSize; // A tile is one full map.

	const northPlots = getPlotsAfterSteps(map, 130, center, 0);
	const westPlots = getPlotsAfterSteps(map, 130, mapEdge, center);
	const eastPlots = getPlotsAfterSteps(map, 130, 0, center);
	const southPlots = getPlotsAfterSteps(map, 130, center, mapEdge);

	const northWestSmall = getPlotsAfterSteps(map, 64, mapEdge, 0);
	const northEastSmall = getPlotsAfterSteps(map, 64, 0, 0);
	const southWestSmall = getPlotsAfterSteps(map, 64, mapEdge, mapEdge);
	const southEastSmall = getPlotsAfterSteps(map, 64, 0, mapEdge);

	const northWestLarge = getPlotsAfterSteps(map, 64 + 131, mapEdge, 0);
	const northEastLarge = getPlotsAfterSteps(map, 64 + 131, 0, 0);
	const southWestLarge = getPlotsAfterSteps(map, 64 + 131, mapEdge, mapEdge);
	const southEastLarge = getPlotsAfterSteps(map, 64 + 131, 0, mapEdge);

	const numberOfEvenTiles = totalTiles**2;
	const numberOfOddTiles = (totalTiles - 1)**2;

	const numberOfEvenPlots = getPlotsAfterSteps(map, 65 + 131, START[0], START[1]);
	const numberOfOddPlots = getPlotsAfterSteps(map,  65 + 131 + 1, START[0], START[1]);

	return (
		northPlots + westPlots + eastPlots + southPlots +
		totalTiles * (northWestSmall + northEastSmall + southWestSmall + southEastSmall) +
		(totalTiles - 1) * (northWestLarge + northEastLarge + southWestLarge + southEastLarge) +
		numberOfEvenTiles * numberOfEvenPlots + numberOfOddTiles * numberOfOddPlots 
	);
}

function main() {
	console.log(part1());
	console.log(part2());
}

main();
