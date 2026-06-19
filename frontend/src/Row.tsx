import type Character from "./types/Character"

interface RowProps {
    character: Character
}

export default function Row({character}: RowProps) {
    return (
        <tr className="row">
            <th scope="row">
                <img src={character.image} className="cell image-cell"></img>
            </th>
            <td className="cell name-cell">{character.name}</td>
            {/* <td className="cell rarity-cell">{character.rarity}</td> */}
            <td className="cell afflatus-cell">{character.afflatus}</td>
            <td className="cell damage-cell">{character.damage === "Real" ? "Reality" : character.damage}</td>
            <td className="cell tags-cell">{character.tags.map((tag) => 
                <div style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center"
                }}>
                    {tag}
                </div>
            )}</td>
        </tr>
    )
}