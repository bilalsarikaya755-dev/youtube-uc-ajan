"""Ajan çıktılarının biçim, kaynak ilişkisi ve süre kontrolleri."""

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator


class Record(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class Source(Record):
    id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    url: HttpUrl
    publication_date: str = Field(min_length=1)
    data_period: str = Field(min_length=1)
    scope: str = Field(min_length=1)


class Fact(Record):
    id: str = Field(min_length=1)
    claim: str = Field(min_length=1)
    source_ids: list[str] = Field(min_length=1)
    limitation: str = Field(min_length=1)


class Research(Record):
    topic: str = Field(min_length=1)
    selection_reason: str = Field(min_length=1)
    demand_status: str = Field(min_length=1)
    sources: list[Source] = Field(min_length=3)
    facts: list[Fact] = Field(min_length=3)
    unknowns: list[str]

    @model_validator(mode="after")
    def check_references(self):
        source_ids = unique_ids(self.sources, "kaynak")
        unique_ids(self.facts, "olgu")
        for fact in self.facts:
            if not set(fact.source_ids) <= source_ids:
                raise ValueError(f"{fact.id}: tanımsız kaynak kullanılmış")
        return self


class Section(Record):
    id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    duration_seconds: int = Field(strict=True, ge=1, le=120)
    narration: str = Field(min_length=1)
    fact_ids: list[str]


class Script(Record):
    title: str = Field(min_length=1)
    thumbnail_text: str = Field(min_length=1)
    main_duration_seconds: int = Field(strict=True, ge=60, le=900)
    sections: list[Section] = Field(min_length=4)
    short_duration_seconds: int = Field(strict=True, ge=15, le=180)
    short_sections: list[Section] = Field(min_length=3)
    description: str = Field(min_length=1)
    pinned_comment: str = Field(min_length=1)

    @model_validator(mode="after")
    def check_timings(self):
        unique_ids(self.sections + self.short_sections, "bölüm")
        for parts, expected in (
            (self.sections, self.main_duration_seconds),
            (self.short_sections, self.short_duration_seconds),
        ):
            if sum(p.duration_seconds for p in parts) != expected:
                raise ValueError("Bölüm süreleri hedef süreyi karşılamıyor")
            for p in parts:
                if len(p.narration.split()) > p.duration_seconds * 3.5:
                    raise ValueError(f"{p.id}: seslendirme süreye göre çok uzun")
        return self


class Shot(Record):
    section_id: str = Field(min_length=1)
    visual: str = Field(min_length=1)
    on_screen: str = Field(min_length=1)
    sound: str = Field(min_length=1)
    asset_note: str = Field(min_length=1)


class Direction(Record):
    main_shots: list[Shot] = Field(min_length=4)
    short_shots: list[Shot] = Field(min_length=3)
    production_notes: list[str] = Field(min_length=1)


def unique_ids(records, label: str) -> set[str]:
    ids = [r.id for r in records]
    if len(ids) != len(set(ids)):
        raise ValueError(f"Yinelenen {label} kimliği")
    return set(ids)


def validate_script(script: Script, research: Research, main_seconds: int,
                    short_seconds: int) -> None:
    if (script.main_duration_seconds, script.short_duration_seconds) != (
        main_seconds, short_seconds
    ):
        raise ValueError("Senaryo istenen video sürelerini değiştirmiş")
    fact_ids = {f.id for f in research.facts}
    for section in script.sections + script.short_sections:
        if not set(section.fact_ids) <= fact_ids:
            raise ValueError(f"{section.id}: araştırmada bulunmayan olgu")


def validate_direction(direction: Direction, script: Script) -> None:
    for shots, parts in ((direction.main_shots, script.sections),
                         (direction.short_shots, script.short_sections)):
        got = [s.section_id for s in shots]
        wanted = {p.id for p in parts}
        if len(got) != len(set(got)) or set(got) != wanted:
            raise ValueError("Yönetmen her bölümü tam bir kez planlamalı")


def extract_output(output: Any, schema):
    if getattr(output, "pydantic", None) is not None:
        return schema.model_validate(output.pydantic.model_dump(mode="json"))
    if getattr(output, "json_dict", None) is not None:
        return schema.model_validate(output.json_dict)
    raw = output.raw.strip()
    if raw.startswith("```") and raw.endswith("```"):
        raw = "\n".join(raw.splitlines()[1:-1])
    return schema.model_validate_json(raw)


def write_json(path: Path, data: dict) -> None:
    """Yarım dosya bırakmadan aynı dizin içinde atomik yaz."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                         encoding="utf-8")
    temporary.replace(path)


def clock(seconds: int) -> str:
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def timeline(parts):
    elapsed = 0
    for part in parts:
        end = elapsed + part.duration_seconds
        yield part, elapsed, end
        elapsed = end


def cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def render_package(research: Research, script: Script, direction: Direction) -> str:
    validate_script(script, research, script.main_duration_seconds,
                    script.short_duration_seconds)
    validate_direction(direction, script)
    lines = [f"# {script.title}", "", f"Kapak metni: **{script.thumbnail_text}**",
             "", "## Konu seçimi", "", research.selection_reason, "",
             f"Talep verisinin sınırı: {research.demand_status}", "",
             "Planlı süreler; kesin zamanlama ses kaydından sonra yapılır.", ""]
    for title, parts, shots in (("Ana video", script.sections, direction.main_shots),
                                ("Shorts", script.short_sections, direction.short_shots)):
        lines += [f"## {title} - seslendirme", ""]
        for part, start, end in timeline(parts):
            refs = ", ".join(part.fact_ids) or "Anlatı / varsayımsal örnek"
            lines += [f"### {clock(start)}-{clock(end)} | {part.title}", "",
                      part.narration, "", f"Editör kaynak notu: {refs}", ""]
        lines += [f"## {title} - kurgu tablosu", "",
                  "| Süre | Bölüm | Görüntü / B-roll | Ekran yazısı | Ses | Materyal notu |",
                  "|---|---|---|---|---|---|"]
        by_id = {s.section_id: s for s in shots}
        for part, start, end in timeline(parts):
            shot = by_id[part.id]
            row = [f"{clock(start)}-{clock(end)}", part.id, shot.visual,
                   shot.on_screen, shot.sound, shot.asset_note]
            lines.append("| " + " | ".join(cell(v) for v in row) + " |")
        lines.append("")
    lines += ["## Yayın metinleri", "", "Açıklama:", "", script.description,
              "", "Sabit yorum:", "", script.pinned_comment, "",
              "## Üretim notları", ""]
    lines += [f"- {note}" for note in direction.production_notes]
    lines += ["", "## Kaynaklar ve kapsam", ""]
    for source in research.sources:
        lines += [f"- **{source.id} - {source.title}**: {source.url}",
                  f"  Yayın: {source.publication_date}. Veri dönemi: {source.data_period}.",
                  f"  Kapsam: {source.scope}"]
    lines += ["", "## Olgu kontrolü", ""]
    for fact in research.facts:
        lines += [f"- **{fact.id}** ({', '.join(fact.source_ids)}): {fact.claim}",
                  f"  Sınır: {fact.limitation}"]
    lines += ["", "## Açık kalanlar", ""]
    lines += [f"- {unknown}" for unknown in research.unknowns]
    return "\n".join(lines) + "\n"
