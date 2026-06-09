import type Character from "./types/Character"

interface RowProps {
    character: Character
}

export default function Row({character}: RowProps) {
    return (
        <div style={{
            display: "flex",
            gap: "100px",
            border: "1px solid black",
            height: "100px",
            justifyContent: "space-around"
        }}>
            <img src={character.image}></img>
            <div>{character.name}</div>
            <div>{character.rarity}</div>
            <div>{character.afflatus}</div>
            <div>{character.damage}</div>
            <div>{character.tags}</div>
        </div>
    )
}