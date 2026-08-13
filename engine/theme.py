from dataclasses import dataclass

@dataclass(frozen=True)
class Theme:
    name: str
    background: str
    text_main: str
    text_sub: str
    hero: str
    muted: str
    negative: str
    grid: str


OBSIDIAN = Theme(
    name="Obsidian",
    background="#0E1117",
    text_main="#FFFFFF",
    text_sub="#888888",
    hero="#00E5FF",
    muted="#222222",
    negative="#FF2E63",
    grid="#333333"
)

MIDNIGHT_GOLD = Theme(
    name="Midnight Gold",
    background="#050A14",
    text_main="#F1F5F9",
    text_sub="#94A3B8",
    hero="#FFD700",
    muted="#1E293B",
    negative="#EF4444",
    grid="#334155"
)

SWISS_CLEAN = Theme(
    name="Swiss Clean",
    background="#FFFFFF",
    text_main="#000000",
    text_sub="#555555",
    hero="#0044CC",
    muted="#EEEEEE",
    negative="#D62828",
    grid="#E5E5E5"
)

THEMES = {
    "Obsidian (Dark Mode)": OBSIDIAN,
    "Midnight Gold (Luxury)": MIDNIGHT_GOLD,
    "Swiss Clean (Light Mode)": SWISS_CLEAN
}