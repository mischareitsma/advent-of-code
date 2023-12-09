import * as fs from "node:fs";
import { dirname } from "path";
import { fileURLToPath } from "url";
import { max, sort } from "../math.js";

const __dirname = dirname(fileURLToPath(import.meta.url));

const isTest = false;

const fname = (isTest ? "test_" : "") + "input.dat";

const lines = fs.readFileSync(__dirname + "/" + fname).toString().split("\n");
lines.pop();


const CARDS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"];
const CARDS_JOKER = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"];

/**
 * Get the type of cards. Types available:
 * 
 * - (7) Five of a kind (all cards the same)
 * - (6) Four of a kind (four cards the same)
 * - (5) Full house (three the same and remaining two the same)
 * - (4) Three of a kind (three the same, other two not the same)
 * - (3) Two pair (Two times two cards the same, remaining not the same)
 * - (2) One pair (Two cards the same, rest different)
 * - (1) High cards (No same cards, all different)
 * 
 * @param {string} cards String of five cards
 * @returns Integer value for the type. Higher number is stronger type.
 */
function getTypeFromCards(cards) {
	getTypeFromCardCounts(getCountsFromCard(cards));
}

function getTypeFromCardCounts(counts) {
	if (counts[0] === 5) return 7;
	if (counts[0] === 4) return 6;
	if (counts[0] === 3) {
		if (counts[1] === 2) return 5;
		else return 4;
	}
	if (counts[0] === 2) {
		if (counts[1] === 2) return 3;
		else return 2;
	}
	return 1;
}

function getCountsFromCard(cards) {
	const countsPerCard = {};
	for (const card of cards) {
		if (card in countsPerCard)
			countsPerCard[card]++;
		else
			countsPerCard[card] = 1;
	}
	const counts = [];
	for (const card in countsPerCard) {
		counts.push(countsPerCard[card]);
	}
	return sort(counts).reverse();
}

function getTypeFromCardsWithJoker(cards) {
	const counts = getCountsFromCard(cards);
	const jokerCount = Array.from(cards).filter(c => c === "J").length;

	const types = [];
	types.push(getTypeFromCardCounts(counts));

	// Remove jokerCount itself
	counts.splice(counts.indexOf(jokerCount), 1);

	// Get all possible types, get the biggest one.

	for (let i = 0; i < counts.length; i++) {
		const newCounts = [...counts];
		newCounts[i] += jokerCount;
		types.push(getTypeFromCardCounts(sort(newCounts).reverse()));
	}
	
	return max(types);
}

const hands = [];
const hands_joker = [];

lines.forEach((line) => {
	const [cards, bid] = line.split(" ");
	hands.push({
		cards: cards,
		bid: Number.parseInt(bid),
		type: getTypeFromCards(cards)
	});
	hands_joker.push({
		cards: cards,
		bid: Number.parseInt(bid),
		type: getTypeFromCardsWithJoker(cards)
	});
});

function handSorter(hand1, hand2, cardOrder) {
	if (hand1.type === hand2.type) {
		for (let i = 0; i < 5; i++) {
			const card1 = hand1.cards[i];
			const card2 = hand2.cards[i];
			if (hand1.cards[i] === hand2.cards[i]) continue;
			// cardOrder array is reversed order in strength
			return cardOrder.indexOf(card2) > cardOrder.indexOf(card1) ? 1 : -1;
		}
		// If we are here, all is equal.
		return 0;
	}

	return hand1.type > hand2.type ? 1 : -1;
}

function getWinnings(hands) {
	let winnings = 0;
	hands.forEach((hand, idx) => winnings += (hand.bid * (idx + 1)));
	return winnings;
}

function part1() {
	hands.sort((h1, h2) => handSorter(h1, h2, CARDS));
	return getWinnings(hands);
}

function part2() {
	hands_joker.sort((h1, h2) => handSorter(h1, h2, CARDS_JOKER));
	return getWinnings(hands_joker);
}

function main() {
	console.log(`Part 1: ${part1()}`);
	console.log(`Part 2: ${part2()}`);
}

main();
