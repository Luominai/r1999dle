import type Character from "./types/Character";
import star from "./assets/star.png"

export default function Results({character, correct, onClose}: {character: Character, correct: boolean, onClose: () => void}) {
    return (
        <div style={{
            position: "absolute",
            width: "100%",
            height: "100%",
            backgroundColor: "#000000b2",
            zIndex: 100,
            display: "flex",
            justifyContent: "center",
            alignItems: "center"
        }}>
            <div style={{
                width: "500px",
                height: "350px",
                maxWidth: "80%",
                maxHeight: "80%",
                backgroundColor: "#212121",
                display: "flex",
                alignItems: "center",
                flexDirection: "column",
                border: "1px solid #d76228",
                position: "relative",
                padding: "16px",
                gap: "8px"
            }}>
                <div style={{
                    width: "100%",
                    display: "flex",
                    justifyContent: "end",
                    paddingRight: "16px"
                }}>
                    <div style={{
                        cursor: "pointer"
                    }}
                    onClick={(_) => onClose()}
                    >
                        Return ⨯
                    </div>
                </div>

                <div style={{
                    fontSize: 24,
                    color: "#df8253"
                }}>
                    {correct ? "Congratulations!" : "Game Over!"} The answer was {character.Name}!
                </div>
                <div style={{display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center"}}>
                    <img src={character.Icon_Small} style={{ 
                        maxHeight: "100%", 
                        maxWidth: "100%", 
                        width: "120px",
                        height: "120px",
                        padding: "8px"
                    }}/>
                    {/* <div>
                        <img src={character.signature} style={{height: "60px"}}></img>
                    </div> */}
                    <div style={{display: "flex", justifyContent: "center", gap: "16px"}}>
                        <div>{Array.from({length: character.Rarity}).map((_) => <img src={star}/>)}</div>
                        <div>{character.Afflatus}</div>
                        <div>{character.DMG_Type}</div>
                    </div>
                    <div style={{display: "flex", gap: "16px"}}>
                        {character.Tags.map((tag) => <span>{tag}</span>)}
                    </div>
                </div>
            </div>
        </div>
    )
}