import { useState } from "react"
import characterData from "./assets/complete.json"
import type Character from "./types/Character"

type onSelectFunction = (c: Character) => any

export default function Dropdown({ onSelect }: { onSelect: onSelectFunction }) {
	const [dropdownVisible, setDropdownVisible] = useState(false)
	const [query, setQuery] = useState("")

	const subset: Array<Character> = Object.values(characterData).filter((data) => {
		return data.name.toLowerCase().startsWith(query.toLowerCase())
	})

	return (
		<div style={{ display: "flex", justifyContent: "center", marginTop: "20px"}}>
			<div style={{display: "flex", flexDirection: "column", minWidth: "200px", flexGrow: 1, maxWidth: "600px"}}>
				<input
					className="text-input"
					type='text'
					value={query}
					placeholder="Enter a character's name"
					onChange={(e) => setQuery(e.target.value)}
					onFocus={(_) => setDropdownVisible(true) }
					onBlur={(_) => setDropdownVisible(false)}
				/>
				{dropdownVisible
					?
					<div style={{ position: "relative", minWidth: "200px", flexGrow: 1, maxWidth: "600px", zIndex: "2"}}>
						<div className="dropdown-container">
							{subset.map((character) =>
								<div className="dropdown-item"
									onMouseDown={(_) => {
										onSelect(character)
										setQuery("")
									}}>
									<img src={character.image} style={{ height: "72px" }}></img>
									{character.name}
								</div>
							)}
						</div>
					</div>
					:
					<></>
				}
			</div>
		</div>
	)
}