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
