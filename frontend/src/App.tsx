import { useState } from 'react'
import './App.css'
import Row from './Row'
import Dropdown from './Dropdown'
import type Character from './types/Character'

function App() {
	const [guesses, setGuesses] = useState<Array<Character>>([])
	return (
		<div>
			<Dropdown onSelect={(selected) => {
				if (!guesses.includes(selected)) {
					setGuesses((g) => g.concat(selected))
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
					{guesses.map((guess) => <Row character={guess} />)}
				</tbody>
			</table>
		</div>
	)
}

export default App
