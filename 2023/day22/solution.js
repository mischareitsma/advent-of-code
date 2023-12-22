import { readFileSync } from "node:fs";
import { dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));

const isTest = false;
const testNumber = "";

const fname = (isTest ? `test${testNumber}_` : "") + "input.dat";

const lines = readFileSync(__dirname + "/" + fname).toString().split("\n");
lines.pop();

class PointSet {

	constructor() {
		/**
		 * Map of points that acts as a set.
		 * 
		 * @type {Map<String,Point>}
		 */
		this.points = new Map();
	}

	/**
	 * Add a point.
	 * 
	 * @param {Point} point Point to add.
	 */
	add(point) {
		if (!this.contains(point)) this.points.set(point.key, point);
	}

	/**
	 * Add all points from other set.
	 * 
	 * This will modify the current set, use union if the original set needs to stay
	 * intact.
	 * 
	 * @param {PointSet} other Other point set
	 */
	addFromSet(other) {
		// Just set, as points should be immutable,
		other.points.forEach((v, k) => this.points.set(k, v));
	}

	/**
	 * Remove a point.
	 * @param {Point} point Point to remove
	 */
	remove(point) {
		this.points.delete(point.key);
	}

	/**
	 * Remove all points from other set.
	 * 
	 * @param {PointSet} other 
	 */
	removeFromSet(other) {
		other.getAsArray().forEach(p => this.remove(p));
	}

	clear() {
		this.points.clear();
	}

	/**
	 * Check if a point is in the set.
	 * 
	 * @param {Point} point Point to check
	 */
	contains(point) {
		return this.points.has(point.key);
	}

	/**
	 * @returns {Point[]} All points in the set as array.
	 */
	getAsArray() {
		return Array.from(this.points.values());
	}

	/**
	 * Create union of the two sets;
	 * @param {PointSet} other Other point set
	 */
	union(other) {
		const newSet = new PointSet();
		newSet.points = new Map([...this.points, ...other.points]);
		return newSet;
	}

	/**
	 * Create intersection.
	 * @param {PointSet} other Other point set
	 */
	intersection(other) {
		const newSet = new PointSet()
		this.points.forEach((v, k) => {
			if (other.contains(k)) newSet.points.set(k, v);
		});
	}

	copy() {
		const newSet = new PointSet();
		newSet.points = new Map([...this.points]);
		return newSet;
	}
}


// Immutable or not immutable? They need to be treated immutable! Otherwise the equals
// just doesn't work? Nope not necessarily, but treat immutable.
class Point {
	/**
	 * @constructor
	 * @param {number} x x-coordinate
	 * @param {number} y y-coordinate
	 * @param {number} z z-coordinate
	 */
	constructor(x, y, z) {
		this.x = x;
		this.y = y;
		this.z = z;
		this.key = `${this.x},${this.y},${this.z}`;
	}

	equals(other) {
		if (!(other instanceof Point))
			return false;

		return this.x === other.x && this.y === other.y && this.z === other.z;
	}

	/**
	 * 
	 * @param {number} dx delta-x
	 * @param {number} dy delta-y
	 * @param {number} dz delta-z
	 * @returns {Point} new point with moved coordinates.
	 */
	move(dx, dy, dz) {
		return new Point(this.x + dx, this.y + dy, this.z + dz);
	}
}

/**
 * @property {Point} start
 * @property {Point} end
 */
class Cube {

	/**
	 * List of cubes this cube is supported by
	 * @type {Cube[]}
	 */
	supportedBy = [];

	/**
	 * List of cubes this cube is supporting
	 * @type {Cube[]}
	 */
	supporting = [];

	/**
	 * Flag that indicates the cube is on the bottom
	 * @type {boolean}
	 */
	reachedBottom = false;

	/**
	 * Flag indicating cube dropped in a round
	 * @type {boolean}
	 */
	hasDropped = false;

	/**
	 * Create a new cube.
	 * 
	 * @constructor
	 * @param {Point} start Starting point
	 * @param {Point} end Ending point
	 */
	constructor(start, end) {

		/**
		 * Start point
		 * @type {Point}
		 */
		this.start = start;

		/**
		 * End point
		 * @type {Point}
		 */
		this.end = end;
		
		/**
		 * List of points in cube
		 * @type {PointSet}
		 */
		this.points = new PointSet();

		/**
		 * List of points one below the current
		 * @type {PointSet}
		 */
		this.pointsBelow = new PointSet();

		this.generatePoints();

	}

	generatePoints(){
		const xStart = Math.min(this.start.x, this.end.x);
		const xEnd = Math.max(this.start.x, this.end.x);

		const yStart = Math.min(this.start.y, this.end.y);
		const yEnd = Math.max(this.start.y, this.end.y);

		const zStart = Math.min(this.start.z, this.end.z);
		const zEnd = Math.max(this.start.z, this.end.z);

		this.reachedBottom = (zStart === 1)

		for (let x = xStart; x <= xEnd; x++) {
			for (let y = yStart; y <= yEnd; y++) {
				for (let z = zStart; z <= zEnd; z++) {
					this.points.add(new Point(x, y, z));
					if (!this.reachedBottom)
						this.pointsBelow.add(new Point(x, y, z-1));
				}
			}
		}
	}

	/**
	 * 
	 * @param {PointSet} otherPoints Obstructions.
	 * @returns {Boolean} **true** if can drop, else **false**;
	 */
	canDrop(otherPoints) {
		for (const point of this.pointsBelow.getAsArray()) {
			if (this.points.contains(point))
				continue;
			if (otherPoints.contains(point)) return false;
		}
		return true;
	}

	drop() {
		this.points.clear();
		this.points.addFromSet(this.pointsBelow);
		this.pointsBelow.clear()
		this.points.getAsArray().forEach(p => {
			if (p.z === 1) this.reachedBottom = true;
			this.pointsBelow.add(p.move(0, 0, -1))
		});
		// TODO: (Mischa Reitsma) Should we clean up the pointsBelow if we reached bottom? now we keep garbage.
	}

	addSupportingCube(cube) {
		if (!this.supporting.includes(cube))
			this.supporting.push(cube);
	}

	addSupportedByCube(cube) {
		if (!this.supportedBy.includes(cube))
			this.supportedBy.push(cube);
	}

	copy() {
		const newCube = new Cube(this.start, this.end);
		newCube.points = this.points.copy();
		newCube.pointsBelow = this.pointsBelow.copy();
		newCube.reachedBottom = this.reachedBottom;

		// These three get the initial values. Copy is done after disintegrations, so need
		// to do these things again.
		newCube.hasDropped = false;
		newCube.supportedBy = [];
		newCube.supporting = [];
		return newCube;
	}
}

class CubeGrid {

	/**
	 * @type {Cube[]} List of disintegrable cubes.
	 */
	disintegrable = []

	/**
	 * Ranges are {min: minValue, max: maxValue}, both are inclusive.
	 */
	constructor(xRange, yRange, zRange, initValue=null) {
		this.xRange = xRange;
		this.yRange = yRange;
		this.zRange = zRange;

		this.xSize = this.xRange.max - this.xRange.min + 1;
		this.ySize = this.yRange.max - this.yRange.min + 1;
		this.zSize = this.zRange.max - this.zRange.min + 1;

		/**
		 * 3D Value grid
		 * @type {Cube[][][]}
		 */
		this.values = new Array(this.xSize);
		
		for (let i = 0; i < this.xSize; i++) {
			this.values[i] = new Array(this.ySize);
			
			for (let j = 0; j < this.ySize; j++) {
				this.values[i][j] = new Array(this.zSize).fill(initValue);
			}
		}

		/**
		 * @type {PointSet}
		 */
		this.points = new PointSet();

		/**
		 * List of cubes.
		 * @type {Cube[]}
		 */
		this.cubes = [];
	}

	/**
	 * @param {Cube} cube 
	 */
	add(cube) {
		cube.points.getAsArray().forEach(p => {
			this.points.add(p);
		});
		this.cubes.push(cube);
	}

	/**
	 * @returns {Cube[]} List of cubes that is save to disintegrate.
	 */
	disintegrable() {
		const disintegrableCubes = [];
		this.cubes.forEach(cube => {
			if (cube.supporting.length === 0) {
				disintegrableCubes.push(cube);
				return;
			}
			let canDisintegrate = true;
			cube.supporting.forEach(supportingCube => {
				if (supportingCube.supportedBy.length === 1)
					canDisintegrate = false;
			});
			if (canDisintegrate)
				disintegrableCubes.push(cube);
		});
		return disintegrableCubes;
	}

	dropCubes() {

		// Reset dropped flags to false;
		this.cubes.forEach(cube => {
			cube.hasDropped = false;
		});

		let stuckCubes = [];

		while (stuckCubes.length !== this.cubes.length) {
			stuckCubes = [];
			this.cubes.forEach(cube => {
				let hasMoved = false;

				while (!cube.reachedBottom && cube.canDrop(this.points)) {
					hasMoved = true;
					this.points.removeFromSet(cube.points);
					cube.drop();
					this.points.addFromSet(cube.points);
				}

				if (!hasMoved)
					stuckCubes.push(cube);
				else
					cube.hasDropped = true;
			});
		}
	}

	// Weird name?
	createInventory() {
		this.cubes.forEach(cube => {
			cube.points.getAsArray().forEach((point) => {
				this.values[point.x][point.y][point.z] = cube;
			});
		});

		this.cubes.forEach(cube => {
			cube.points.getAsArray().forEach((point) => {
				if (point.z + 1 >= this.zSize) return
				const possibleCube = this.values[point.x][point.y][point.z + 1];

				if (possibleCube && cube !== possibleCube) {
					cube.addSupportingCube(possibleCube);
					possibleCube.addSupportedByCube(cube);
				}
			});
		});
		
		this.cubes.forEach(cube => {

			if (cube.supporting.length === 0) {
				this.disintegrable.push(cube);
				return;
			}

			let canDisintegrate = true;

			cube.supporting.forEach(supportingCube => {
				if (supportingCube.supportedBy.length === 1)
					canDisintegrate = false;
			});

			if (canDisintegrate)
				this.disintegrable.push(cube);
		});

	}

	/**
	 * Return a cube using it's index number.
	 * @param {number} idx Cube number
	 * @returns {Cube} cube from cubes array.
	 */
	getCube(idx) {
		return this.cubes[idx];
	}

	/**
	 * Disintegrate a cube.
	 * @param {Cube} cube Cube to disintegrate.
	 */
	disintegrateCube(cube) {
		this.disintegrable.splice(this.disintegrable.indexOf(cube), 1);
		this.cubes.splice(this.cubes.indexOf(cube), 1);
		this.points.removeFromSet(cube.points);
	}

	copy() {
		const newCubeGrid = new CubeGrid(this.xRange, this.yRange, this.zRange);
		this.cubes.forEach(cube => newCubeGrid.add(cube.copy()));
		newCubeGrid.createInventory();
		return newCubeGrid;
	}
}

const cubes = [];

const xRange = {min: 1e99, max: -1}
const yRange = {min: 1e99, max: -1}
const zRange = {min: 0, max: -1}

lines.forEach(line => {
	const [p1, p2] = line.split("~");
	const [x1, y1, z1] = p1.split(",").map(v => Number.parseInt(v));
	const [x2, y2, z2] = p2.split(",").map(v => Number.parseInt(v));

	xRange.min = Math.min(xRange.min, x1, x2);
	xRange.max = Math.max(xRange.max, x1, x2);

	yRange.min = Math.min(yRange.min, y1, y2);
	yRange.max = Math.max(yRange.max, y1, y2);

	zRange.min = Math.min(zRange.min, z1, z2);
	zRange.max = Math.max(zRange.max, z1, z2);

	cubes.push(new Cube(
		new Point(x1, y1, z1),
		new Point(x2, y2, z2)
	));
});

const cubeGrid = new CubeGrid(xRange, yRange, zRange);
cubes.forEach(cube => cubeGrid.add(cube));

cubeGrid.dropCubes();
cubeGrid.createInventory();

function part1() {
	return cubeGrid.disintegrable.length;
}

function part2() {
	let total = 0;
	for (let i = 0; i < cubeGrid.cubes.length; i++) {
		const cubeGridCopy = cubeGrid.copy();
		cubeGridCopy.disintegrateCube(cubeGridCopy.getCube(i));
		cubeGridCopy.dropCubes();
		total += cubeGridCopy.cubes.filter(cube => cube.hasDropped).length;
	}
	return total;
}

function main() {
	const answerPart1 = part1();
	const testPart1 = 5
	console.log(`Part 1: ${answerPart1} (test${!isTest ? "" : testPart1 === answerPart1 ? " OK" : " NOK"}: ${testPart1})`);

	const answerPart2 = part2();
	const testPart2 = 7;
	console.log(`Part 1: ${answerPart2} (test${!isTest ? "" : testPart2 === answerPart2 ? " OK" : " NOK"}: ${testPart2})`);
}

main();
