import characterData from "./assets/merged.json"
import type Character from "./types/Character"

type onSelectFunction = (c: Character) => any

export default function Dropdown({query, onSelect} : {query : string, onSelect: onSelectFunction}) {
    //@ts-ignore
    const subset: Array<Character> = Object.values(characterData).filter((data) => {
        return data.name.toLowerCase().startsWith(query.toLowerCase())
    })

    return (
        <div style={{width: "100%", display: "flex", justifyContent: "center"}}>
            <div style={{position: "relative", minWidth: "200px", flexGrow: 1, maxWidth: "600px"}}>
                <div style={{
                    position: "absolute", 
                    maxHeight: "300px", 
                    overflowY: "scroll",
                    boxSizing: "border-box",
                    border: "1px solid #B55829",
                    backgroundColor: "#212121",
                    color: "#c07d5c",
                    width: "100%"
                }}>
                    {subset.map((character) => 
                        <div style={{
                            display: "flex",
                            justifyContent: "start",
                            alignItems: "center",
                            gap: "20px",
                            padding: "4px"
                        }}
                        onMouseDown={(e) => {
                            onSelect(character)
                            console.log(character.name)
                        }}>
                            <img src={character.image} style={{height: "72px"}}></img>
                            {character.name}
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}