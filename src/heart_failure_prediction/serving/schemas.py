from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class SexEnum(str, Enum):
    M = 'M'
    F = 'F'


class ChestPainTypeEnum(str, Enum):
    TA = 'TA'  # Typical Angina
    ATA = 'ATA'  # Atypical Angina
    NAP = 'NAP'  # Non-Anginal Pain
    ASY = 'ASY'  # Asymptomatic


class RestingECGEnum(str, Enum):
    Normal = 'Normal'
    ST = 'ST'  # having ST-T wave abnormality
    LVH = 'LVH'  # showing probable or definite left ventricular hypertrophy


class ExerciseAnginaEnum(str, Enum):
    Y = 'Y'
    N = 'N'


class STSlopeEnum(str, Enum):
    Up = 'Up'
    Flat = 'Flat'
    Down = 'Down'


class HeartDiseaseRecord(BaseModel):
    Age: int = Field(..., gt=0, description='Age of the patient [years]')

    Sex: SexEnum = Field(..., description='Sex of the patient [M: Male, F: Female]')

    ChestPainType: ChestPainTypeEnum = Field(
        ...,
        description='Chest pain type [TA: Typical Angina, ATA: Atypical Angina, '
        'NAP: Non-Anginal Pain, ASY: Asymptomatic]',
    )

    RestingBP: int = Field(..., gt=0, description='Resting blood pressure [mm Hg]')

    Cholesterol: int | None = Field(
        default=None, ge=0, description='Serum cholesterol [mm/dl]'
    )

    FastingBS: Literal[0, 1] = Field(
        ...,
        description='Fasting blood sugar [1: if FastingBS > 120 mg/dl, 0: otherwise]',
    )

    RestingECG: RestingECGEnum = Field(
        ..., description='Resting electrocardiogram results [Normal, ST, LVH]'
    )

    MaxHR: int = Field(
        ...,
        ge=60,
        le=202,
        description='Maximum heart rate achieved [Numeric value between 60 and 202]',
    )

    ExerciseAngina: ExerciseAnginaEnum = Field(
        ..., description='Exercise-induced angina [Y: Yes, N: No]'
    )

    Oldpeak: float = Field(
        ..., description='Oldpeak = ST [Numeric value measured in depression]'
    )

    ST_Slope: STSlopeEnum = Field(
        ...,
        alias='ST_Slope',
        description='The slope of the peak exercise ST segment '
        '[Up: upsloping, Flat: flat, Down: downsloping]',
    )

    class Config:
        populate_by_name = True
        json_schema_extra = {
            'example': {
                'Age': 45,
                'Sex': 'M',
                'ChestPainType': 'ATA',
                'RestingBP': 130,
                'Cholesterol': 230,
                'FastingBS': 0,
                'RestingECG': 'Normal',
                'MaxHR': 140,
                'ExerciseAngina': 'N',
                'Oldpeak': 1.5,
                'ST_Slope': 'Flat',
            }
        }
