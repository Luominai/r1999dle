import type Character from "./types/Character"
import characterData from "./assets/data.json"

const characters: Array<Character> = Object.values(characterData)

export function compare(char1: Character, char2: Character) {
	const output = {
		image: char1.Image === char2.Image,
		name: char1.Name === char2.Name,
		rarity: char1.Rarity === char2.Rarity,
		afflatus: char1.Afflatus === char2.Afflatus,
		damage: char1.DMG_Type === char2.DMG_Type,
		tags: -1,
		release: char1.Version === char2.Version ? 0 : Math.sign(characters.indexOf(char1) - characters.indexOf(char2))
	}

	// return 1 if the 2 characters have the same tags
	if (char1.Tags.length === char2.Tags.length && char1.Tags.every((tag) => char2.Tags.includes(tag))) {
		output.tags = 1
	}
	// return 0 if the tags are not identical, but character 1 shares some tags with character 2
	else if (char1.Tags.some((tag) => char2.Tags.includes(tag))) {
		output.tags = 0
	}

	return output
}

export function toDate(dateString: string) {
	const monthToNumber: Record<string, number> = {
		"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
		"July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
	}
	let [month, day, year] = dateString.split(" ")
	const monthNumber = monthToNumber[month]
	const dayNumber = Number(day.substring(0, day.length - 2))
	const yearNumber = Number(year)
	return new Date(yearNumber, monthNumber, dayNumber)
}