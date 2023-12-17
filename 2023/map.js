/* Notes
Want to generalize this grid concept. Add things like:
- include diagonal to neighbors on input
- add functions for is neighbor reachable
- wrapping onto itself
- Add unreachable boundary so checks like (0 < x < width) are unnecessary
- Rotation/translations?
*/

export class Grid2D {
	/**
	 * Width of the grid.
	 */
	width = 0;

	/**
	 * Height of the grid.
	 */
	height = 0;

	/**
	 * Values of the grid.
	 * 
	 * The values of the grid are stored in a 1D array. The method {@link getIndex()} is used
	 * to translate x and y coordinates to the correct index.
	 */
	values = [];

	/**
	 * Initialize values of the grid.
	 * 
	 * @constructor
	 * @param {number} width Width of the grid
	 * @param {number} height Height of the grid
	 */
	constructor(width, height, initValue) {
		this.setWidth(width);
		this.setHeight(height)
		this.values = new Array(this.width * this.height);
		if (initValue != null)
			this.values.fill(initValue);
	}

	/**
	 * Translate x and y coordinate to index of the values array.
	 * 
	 * @param {number} x x-coordinate
	 * @param {number} y y-coordinate
	 * @returns {number} Index corresponding with the x and y coordinate.
	 */
	getIndex(x, y) {
		return y * this.width + x;
	}

	/**
	 * Translate the index of the values array to an x and y coordinate.
	 * 
	 * @param {number} index Index of the value array
	 * @returns {number[]} Array with x and y as first and second element.
	 */
	getCoords(index) {
		const x = index % this.width;
		return [x, (index - x) / this.width]
	}

	/**
	 * Set the width of the grid.
	 * 
	 * @param {number} width Width of the grid
	 * @throws Width should be greater than 0
	 */
	setWidth(width) {
		if (!(width > 0)) throw new Error(`Width ${width} should be greater than 0`);
		this.width = width
	}

	/**
	 * Set the height of the grid.
	 * 
	 * @param {number} height Height of the grid
	 * @throws Height should be greater than 0
	 */
	setHeight(height) {
		if (!(height > 0)) throw new Error(`Height ${height} should be greater than 0`);
		this.height = height
	}

	/**
	 * Get value on the grid with the **x** and **y** coordinates from the parameters.
	 * 
	 * @param {number} x x-coordinate
	 * @param {number} y y-coordinate
	 * @returns Value in the grid on **(x, y)**
	 */
	getValue(x, y) {
		this.checkValidCoord(x, y);

		return this.values[this.getIndex(x, y)];
	}

	/**
	 * Get a value from the grid using the **x** and **y** coordinates from the parameters.
	 * 
	 * @param {number} x x-coordinate
	 * @param {number} y y-coordinate
	 * @param {any} value Value in the grid corresponding with the x and y coordinate
	 */
	setValue(x, y, value) {
		this.checkValidCoord(x, y);

		this.values[this.getIndex(x, y)] = value;
	}

	/**
	 * Increment a value in the grid. This assumes that the content of the grid are numbers.
	 * 
	 * @param {number} x x-coordinate
	 * @param {number} y y-coordinate
	 * @param {number} value increment value
	 */
	increment(x, y, value=1) {
		this.values[this.getIndex(x, y)] += value;
	}

	/**
	 * Update a value in the grid using an input value and a function that does the update.
	 * 
	 * @param {number} x x-coordinate
	 * @param {number} y y-coordinate
	 * @param {any} value Input value used for an update
	 * @param {Function} fn Function to update the value. New value is set to the return value
	 *                      of this function. Function will be called with current and input
	 *                      values as parameter.
	 */
	updateValue(x, y, value, fn) {
		this.checkValidCoord(x, y);
		
		const idx = this.getIndex(x, y);

		this.values[idx] = fn(this.values[idx], value);
	}

	/**
	 * Check if the **x** and **y** coordinates are valid coordinates.
	 * 
	 * @param {number} x x-coordinate
	 * @param {number} y y-coordinate
	 * @throws x-coordinate should be in range [0, {@link width}]
	 * @throws y-coordinate should be in range [0, {@link height}]
	 */
	checkValidCoord(x, y) {
		if (!this.validX(x))
			throw new Error(`Invalid x ${x}, should be in range [0, ${this.width}]`);

		if (!this.validY(y))
			throw new Error(`Invalid y ${y}, should be in range [0, ${this.height}]`);
	}

	validX(x) {
		return (x >= 0 && x < this.width);
	}

	validY(y) {
		return (y >= 0 && y < this.height);
	}

	validCoords(x, y) {
		return this.validX(x) && this.validY(y);
	}

	/**
	 * Print the grid.
	 */
	print() {
		for (let y = 0; y < this.height; y++) {
			for (let x = 0; x < this.width; x++) {
				process.stdout.write(`${this.getValue(x, this.height - 1 - y)}`);
			}
			process.stdout.write("\n");
		}
	}

	/**
	 * Create a Grid2D object from an array of strings.
	 * 
	 * @param {string[]} lines Array with lines, each line a string of characters.
	 * @returns {Grid2D} Grid with values set from lines array.
	 */
	static from_lines(lines, converter = v => v) {
		const grid = new Grid2D(lines[0].length, lines.length);

		lines.forEach((line, idx) => {
			for (let i = 0; i < line.length; i++) {
				grid.setValue(i, grid.height - idx - 1, converter(line[i]));
			}
		});
		
		return grid;
	}
}
