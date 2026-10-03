#!/usr/bin/env python3
"""
Configuration System for C4C Homework Solver

Manages student info, course settings, and template preferences.
Supports both YAML config files and command-line overrides.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class StudentConfig:
    """Student information."""
    name: str = "Student"
    student_id: str = ""
    email: str = ""
    university: str = ""


@dataclass
class CourseConfig:
    """Course information."""
    name: str = "Mathematics"
    code: str = ""
    semester: str = ""
    instructor: str = ""


@dataclass
class TemplateConfig:
    """LaTeX template preferences."""
    title: str = "Homework Solutions"
    language: str = "en"  # en, zh
    show_steps: bool = True
    show_verification: bool = True
    compact_mode: bool = False
    font_size: str = "11pt"
    margin: str = "1in"


@dataclass
class SolverConfig:
    """Solver preferences."""
    prefer_llm: bool = False
    llm_backend: str = "file"  # dashscope, openai, file
    timeout_seconds: int = 30
    max_retries: int = 3


@dataclass
class Config:
    """Main configuration container."""
    student: StudentConfig
    course: CourseConfig
    template: TemplateConfig
    solver: SolverConfig
    output_dir: str = "output"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "student": asdict(self.student),
            "course": asdict(self.course),
            "template": asdict(self.template),
            "solver": asdict(self.solver),
            "output_dir": self.output_dir,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Config':
        """Create from dictionary."""
        return cls(
            student=StudentConfig(**data.get("student", {})),
            course=CourseConfig(**data.get("course", {})),
            template=TemplateConfig(**data.get("template", {})),
            solver=SolverConfig(**data.get("solver", {})),
            output_dir=data.get("output_dir", "output"),
        )


class ConfigManager:
    """Manage configuration loading and saving."""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = Path(config_path) if config_path else Path("config.yaml")
        self.config: Optional[Config] = None

    def load(self) -> Config:
        """Load configuration from file or create default."""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                if self.config_path.suffix in ['.yaml', '.yml']:
                    data = yaml.safe_load(f)
                else:
                    data = json.load(f)
            self.config = Config.from_dict(data)
        else:
            self.config = Config(
                student=StudentConfig(),
                course=CourseConfig(),
                template=TemplateConfig(),
                solver=SolverConfig(),
            )
        return self.config

    def save(self, config: Optional[Config] = None):
        """Save configuration to file."""
        if config:
            self.config = config

        if not self.config:
            raise ValueError("No configuration to save")

        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.config_path, 'w', encoding='utf-8') as f:
            if self.config_path.suffix in ['.yaml', '.yml']:
                yaml.dump(self.config.to_dict(), f, default_flow_style=False, allow_unicode=True)
            else:
                json.dump(self.config.to_dict(), f, indent=2, ensure_ascii=False)

    def update(self, **kwargs):
        """Update configuration with keyword arguments."""
        if not self.config:
            self.load()

        # Update nested configs
        if "student_name" in kwargs:
            self.config.student.name = kwargs.pop("student_name")
        if "course_name" in kwargs:
            self.config.course.name = kwargs.pop("course_name")
        if "title" in kwargs:
            self.config.template.title = kwargs.pop("title")

        # Update output dir
        if "output_dir" in kwargs:
            self.config.output_dir = kwargs.pop("output_dir")

        return self.config


def create_default_config(output_path: str = "config.yaml"):
    """Create a default configuration file."""
    manager = ConfigManager(output_path)
    config = manager.load()
    manager.save(config)
    print(f"Created default config: {output_path}")
    return config


def load_config(config_path: Optional[str] = None) -> Config:
    """Load configuration from file."""
    manager = ConfigManager(config_path)
    return manager.load()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        output_path = sys.argv[1]
    else:
        output_path = "config.yaml"

    create_default_config(output_path)
