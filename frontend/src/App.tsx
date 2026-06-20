import { useState } from 'react'
import './App.css'
import Row from './Row'
import Dropdown from './Dropdown'
import type Character from './types/Character'
import bg from "./assets/Hongshan_Forest_Zoo_Collab_Special_Art_01.webp"
import Rand from 'rand-seed';
import characterData from "./assets/merged.json"
import Results from './Results'

const today = new Date().toDateString()
const rand = new Rand(today)
const characters = Object.values(characterData)
const dailyCharacter = characters[Math.floor(rand.next() * characters.length)]

function App() {
	const [guesses, setGuesses] = useState<Array<Character | undefined>>([undefined, undefined, undefined, undefined, undefined])
	const [completed, setCompleted] = useState<boolean>(localStorage.getItem("completed") !== null)
	const [correct, setCorrect] = useState<boolean>(localStorage.getItem("correct") === "true")
	const [resultsPageOpen, setResultsPageOpen] = useState<boolean>(false)

	function compare(char1: Character, char2: Character) {
		if (char1 === undefined) {
			return undefined
		}
		
		const output = {
			image: char1.image === char2.image,
			name: char1.name === char2.name,
			rarity: char1.rarity === char2.rarity,
			afflatus: char1.afflatus === char2.afflatus,
			damage: char1.damage === char2.damage,
			tags: -1
		}

		// return 1 if the 2 characters have the same tags
		if (char1.tags.length === char2.tags.length && char1.tags.every((tag) => char2.tags.includes(tag))) {
			output.tags = 1
		}
		// return 0 if the tags are not identical, but character 1 shares some tags with character 2
		else if (char1.tags.some((tag) => char2.tags.includes(tag))) {
			output.tags = 0
		}

		return output
	}

	return (
		<div style={{
			backgroundImage: `url(${bg})`,
			backgroundSize: "cover",
			position: "relative"
		}}>
			{
				completed && resultsPageOpen
				? 
					<Results character={dailyCharacter} correct={correct} onClose={() => setResultsPageOpen(false)}/>
				:
					<></>
			}

			<div style={{
				width: "875px",
				maxWidth: "100%",
				margin: "0 auto",
				textAlign: "center",
				minHeight: "100svh",
				display: "flex",
				flexDirection: "column",
				boxSizing: "border-box"
			}}>
				<Dropdown onSelect={(selected) => {
					if (guesses.includes(selected)) {
						return
					}

					if (completed) {
						return
					}

					const indexOfUndefined = guesses.findIndex((val) => val === undefined)
					if (indexOfUndefined !== -1) {
						const copy = guesses.slice()
						copy[indexOfUndefined] = selected
						setGuesses(copy)
					}

					if (indexOfUndefined === guesses.length - 1) {
						setCompleted(true)
					}

					// if every value is truthy, we have the correct answer
					if (Object.values(compare(selected, dailyCharacter)).every((val) => val == true)) {
						setCompleted(true)
						setCorrect(true)
					}
				}} />

				<table>
					<thead>
						<tr className='row'>
							<th scope='col'>Image</th>
							<th scope='col'>Name</th>
							<th scope='col'>Rarity</th>
							<th scope='col'>Afflatus</th>
							<th scope='col'>Damage</th>
							<th scope='col'>Tags</th>
						</tr>
					</thead>
					<tbody>
						{/* @ts-ignore */}
						{guesses.map((guess) => <Row character={guess} correctness={compare(guess, dailyCharacter)}/>)}
					</tbody>
				</table>

				{
					completed 
					?
						<div style={{display: "flex", justifyContent: "end"}}>
							<div className="button" onClick={(_) => setResultsPageOpen(true)}>
								See Results
							</div>
						</div>
					:
						<></>
				}
			</div>
		</div>
	)
}

export default App
