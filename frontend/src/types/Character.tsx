import type Voiceline from "./Voiceline"

interface Dict {
    [key: string]: any
}

export default interface Character extends Dict {
    ID: number,
    Name: string,
    Version: string,
    Rarity: number,
    Afflatus: string,
    Race: string,
    DMG_Type: String,
    Gender: string,
    Archetypes: Array<string>,
    Other_Name: string,
    Icon_Small: string,
    Era: string
    Location: string,
    Voicelines: {
        First_Encounter: Voiceline,
        Suitcase_Climate: Voiceline,
        To_the_Future: Voiceline,
        Idle: Voiceline,
        Greetings: Voiceline,
        Morning: Voiceline,
        Bond_Morning: Voiceline,
        Night: Voiceline,
        Bond_Night: Voiceline,
        Hat_and_Hair: Voiceline,
        Sleeves_and_Hands: Voiceline,
        Clothing_and_Torso: Voiceline,
        Hobby: Voiceline,
        Praise: Voiceline,
        Intimacy: Voiceline,
        Chitchat_I: Voiceline,
        Chitchat_II: Voiceline,
        Monologue: Voiceline,
        Deployment: Voiceline,
        PreBattle: Voiceline,
        Select_Incantation_I: Voiceline,
        Select_Incantation_II: Voiceline,
        Select_3star_Incantation: Voiceline,
        Select_Ultimate: Voiceline,
        Cast_Arcane_Skill_I: Voiceline,
        Cast_Arcane_Skill_II: Voiceline,
        Cast_Ultimate: Voiceline,
        Attacked_I?: Voiceline,
        Attacked_II?: Voiceline,
        Battle_Victory: Voiceline,
        Insight: Voiceline,
        Bottom_of_Insight?: Voiceline
    }
}