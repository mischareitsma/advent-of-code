import { readFileSync } from "node:fs";
import { dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { stringToNumberArray } from "../utils.js"
import { init } from "z3-solver";

const __dirname = dirname(fileURLToPath(import.meta.url));

const isTest = false;
const testNumber = "";

const LOWER_BOUND = isTest ? 7 : 200000000000000
const UPPER_BOUND = isTest ? 27 : 400000000000000

const fname = (isTest ? `test${testNumber}_` : "") + "input.dat";

const lines = readFileSync(__dirname + "/" + fname).toString().split("\n");
lines.pop();

class Vector {

	/**
	 * 
	 * @param {number} x x component
	 * @param {number} y y component
	 * @param {number} z z-component
	 */
	constructor(x, y, z) {

		/**
		 * @type {number}
		 */
		this.x = x;
		/**
		 * @type {number}
		 */
		this.y = y;
		/**
		 * @type {number}
		 */
		this.z = z;
	}

	/**
	 * @static
	 * @param {string} line 
	 * @param {string} sep 
	 * @returns {Vector}
	 */
	static fromLine(line, sep=", ") {
		const coords = stringToNumberArray(line, sep);
		return new Vector(coords[0], coords[1], coords[2]);
	}

	/**
	 * Add two vectors, returns the result.
	 * @param {Vector} other Vector to add
	 * @returns {Vector} New vector
	 */
	add(other) {
		return new Vector(this.x + other.x, this.y + other.y, this.z + other.z)
	}

	scalarMultiply(c) {
		return new Vector(c * this.x, c * this.y, c * this.z);
	}

	equals(other) {
		return (this.x === other.x && this.y == other.y && this.z === other.z);
	}

	isParallel(other) {
		const ratio = this.x / other.x;

		return (this.x === other.x * ratio) &&
			(this.y === other.y * ratio) &&
			(this.z === other.z * ratio)
	}

	copy() {
		return new Vector(this.x, this.y, this.z);
	}
}

class Intersection {
	constructor(point, time1, time2, isParallel, hailStone1, hailStone2) {
		this.point = point;
		this.time1 = time1;
		this.time2 = time2;
		this.isParallel = isParallel;
		this.hailStone1 = hailStone1;
		this.hailStone2 = hailStone2;
	}
}

class HailStone {
	/**
	 * 
	 * @param {Vector} position Starting position
	 * @param {Vector} velocity Starting velocity
	 */
	constructor(position, velocity) {

		/**
		 * @type {Vector}
		 */
		this.position = position;
		/**
		 * @type {Vector}
		 */
		this.velocity = velocity;

		this.x = this.position.x;
		this.y = this.position.y;
		this.z = this.position.z;

		this.vx = this.velocity.x;
		this.vy = this.velocity.y;
		this.vz = this.velocity.z;
	}

	/**
	 * Return path intersection coordinates of two hailstones.
	 * @param {HailStone} other Other hailstone
	 * @returns {Intersection | null} intersection points.
	 */
	pathIntersection2D(other) {
		// Do lin algebra to solve in 3D, times do not have to be
		// equal.

		const isParallel = this.velocity.isParallel(other.velocity)

		if (isParallel) {
			// TODO: check if the trajectories are the same. Easy, just
			// take this.x, calculate t for other.x and use that t for y and
			//z, then check this.x, this.y and this.z to others.
			// x = x0 + vt, x x = other.x, t = (other.x - this.x) / this.v
			const t = (other.x - this.x) / this.vx;

			// At the t calculated, the y and z coordinates are not equal, then they are
			// parallel and do not intersect. If they do intersect, they intersect over
			// the full line, so the point we take is just the other point at t=0
			if ((other.y !== this.y + this.vy * t) || (other.z !== this.z + this.vz * t))
				return null;
			else {
				return new Intersection(other.point, 0, t, isParallel);
			}
		}

		const [time1, time2] = solveLinearEquation2D(
			[[this.vx, -other.vx], [this.vy, -other.vy]],
			[other.x - this.x, other.y-this.y]
		);

		return new Intersection(
			this.position.add(this.velocity.scalarMultiply(time1)),
			time1,
			time2,
			isParallel,
			this,
			other
		)
	}

	copy() {
		return new HailStone(this.position.copy, this.velocity.copy);
	}
}

function solveLinearEquation2D(m, c) {
	// User Cramer's rule
	const det = determinant2D(m);
	const det1 = determinant2D([[c[0], m[0][1]], [c[1], m[1][1]]]);
	const det2 = determinant2D([[m[0][0], c[0]], [m[1][0], c[1]]]);

	return [det1/det, det2/det];
}

function determinant2D(m) {
	return m[0][0]*m[1][1] - m[0][1]*m[1][0];
}

/**
 * @type {HailStone[]}
 */
const hailStones = lines.map(l => {
	// 19, 13, 30 @ -2,  1, -2
	const splitLine = l.split(" @ ");
	return new HailStone(Vector.fromLine(splitLine[0]), Vector.fromLine(splitLine[1]));
});

function inBounds(v) {
	return v.x >= LOWER_BOUND && v.x <= UPPER_BOUND &&
		v.y >= LOWER_BOUND && v.y <= UPPER_BOUND;
}

function part1() {

	let intersections = [];

	for (let i = 0; i < hailStones.length - 1; i++) {
		for (let j = i+1; j < hailStones.length; j++) {
			const intersection = hailStones[i].pathIntersection2D(hailStones[j]);
			if (intersection)
				intersections.push(intersection);
		}
	}

	const validIntersection = intersections.filter(v => inBounds(v.point) && v.time1 > 0 && v.time2 > 0)

	return validIntersection.length;
}

async function part2() {
	// Use Z3, never did that before :-) Could take a few hours do it by hand, but that would
	// be a pain. Only need 3 hailstones. as it'll give me 9 equations and 9 unknowns (position
	// and velocity of rock, and the three times). Rest of the hailstones have to be fine,
	// otherwise the problem is unsolvable :-)

	const Z3 = await init();
	const ctx = new Z3.Context("main");

	const x = ctx.Real.const("x");
	const y = ctx.Real.const("y");
	const z = ctx.Real.const("z");
	const vx = ctx.Real.const("vx");
	const vy = ctx.Real.const("vy");
	const vz = ctx.Real.const("vz");

	const solver = new ctx.Solver();

	hailStones.slice(0, 3).forEach((hailStone, index) => {
		const t = ctx.Real.const(`t${index}`)
		const xh = hailStone.x;
		const yh = hailStone.y;
		const zh = hailStone.z;
		const vxh = hailStone.vx;
		const vyh = hailStone.vy;
		const vzh = hailStone.vz;
		solver.add(t.ge(0));
		solver.add(x.add(vx.mul(t)).eq(t.mul(vxh).add(xh)));
		solver.add(y.add(vy.mul(t)).eq(t.mul(vyh).add(yh)));
		solver.add(z.add(vz.mul(t)).eq(t.mul(vzh).add(zh)));
	});

	const result = await solver.check()

	if (result !== 'sat')
		throw new Error("Couldn't find a solution")

	const model = solver.model();

	return Number.parseInt(model.get(x)) + Number.parseInt(model.get(y)) + Number.parseInt(model.get(z));
}

async function main() {
	const answerPart1 = part1();
	const testPart1 = 2
	console.log(`Part 1: ${answerPart1} (test${!isTest ? "" : testPart1 === answerPart1 ? " OK" : " NOK"}: ${testPart1})`);

	const answerPart2 = await part2();
	const testPart2 = 47;
	console.log(`Part 1: ${answerPart2} (test${!isTest ? "" : testPart2 === answerPart2 ? " OK" : " NOK"}: ${testPart2})`);
}

main().then(
	() => {
		process.exit(0);
	}
).catch(
	(err) => {
		console.error(`Error: + ${err}`);
		process.exit(1);
	}
);
