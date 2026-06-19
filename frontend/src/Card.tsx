import type Character from "./types/Character";

export default function Card({character}: {character: Character}) {
    return (
        <div style={{
            display: "flex",
            flexDirection: "column",
            height: "40px",
            width: "40px"
        }}>
            <img src={character.image}></img>
            <div>{character.name}</div>
        </div>
    )
}