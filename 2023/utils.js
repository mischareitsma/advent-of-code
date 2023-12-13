/**
 * Transform a string with a list of numbers to an array with numbers.
 * 
 * Examples:
 *
 * - The string `"1, 2, 3"` and delimiter `", "` returns `[1, 2, 3]`.
 * - The string `"4 5 6"` and no delimiters returns `[4, 5, 6]`.
 * 
 * @param {string} s String of numbers
 * @param {string} d Optional delimiter. Default is `" "`
 * @returns Array of numbers
 */
export function stringToNumberArray(s, d=" ") {
	return s.split(d).filter(e => e !== "").map(e => Number.parseInt(e));
}


/**
 * Check if two arrays are equal. The arrays are equal if both are an array,
 * the lengths are equal, and for each index the elements in both arrays are equal.
 * 
 * @param {any[]} a First array
 * @param {any[]} b Second array
 * @returns True if two arrays are equal, false otherwise
 */
export function arraysAreEqual(a, b) {
	if (!Array.isArray(a)) return false;
	if (!Array.isArray(b)) return false;
	if (a.length !== b.length) return false;

	for (let i = 0; i < a.length; i++) {
		if (a[i] !== b[i]) return false;
	}

	return true;
}


/**
 * Generate permutations of a given input array. This is stole from
 * https://stackoverflow.com/questions/9960908/permutations-in-javascript
 * 
 * @param {any[]} inputArr Input array from which to generate permutations
 * @returns {any[][]} Array of permutations of the input array.
 */
export function permutations(inputArr) {
	let result = [];

	const permute = (arr, m = []) => {
		if (arr.length === 0) {
			result.push(m)
		} else {
			for (let i = 0; i < arr.length; i++) {
				let curr = arr.slice();
				let next = curr.splice(i, 1);
				permute(curr.slice(), m.concat(next))
			}
		}
	}

	permute(inputArr)

	return result;
}
