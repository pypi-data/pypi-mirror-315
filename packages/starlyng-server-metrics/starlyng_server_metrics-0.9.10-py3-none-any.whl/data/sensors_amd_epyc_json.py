"""
sensors json response for amd cpu
"""
from typing import Dict

cpu_amd_json_dict: Dict[str, str] = {
    'k10temp-pci-00c3': {
        'Adapter': 'PCI adapter', 
        'Tctl': {
            'temp1_input': 41.625
        },
        'Tccd1': {
            'temp3_input': 41.5
        },
        'Tccd3': {
            'temp5_input': 41.7
        },
        'Tccd5': {
            'temp7_input': 39.5
        },
        'Tccd7': {
            'temp9_input': 42.0
        }
    },
    'nvme-pci-4100': {
        'Adapter': 'PCI adapter',
        'Composite': {
            'temp1_input': 34.85,
            'temp1_max': 81.85,
            'temp1_min': -273.15,
            'temp1_crit': 84.85,
            'temp1_alarm': 0.0
        },
        'Sensor 1': {
            'temp2_input': 34.85,
            'temp2_max': 65261.85,
            'temp2_min': -273.15
        },
        'Sensor 2': {
            'temp3_input': 37.85,
            'temp3_max': 65261.85,
            'temp3_min': -273.15
        }
    },
    'bnxt_en-pci-4200': {
        'Adapter': 'PCI adapter',
        'temp1': {
            'temp1_input': 43.0
        }
    },
    'nct6779-isa-0290': {
        'Adapter': 'ISA adapter',
        'Vcore': {
            'in0_input': 0.6,
            'in0_min': 0.0,
            'in0_max': 1.744,
            'in0_alarm': 0.0,
            'in0_beep': 0.0
        },
        'in1': {
            'in1_input': 0.224,
            'in1_min': 0.0,
            'in1_max': 0.0,
            'in1_alarm': 1.0,
            'in1_beep': 0.0
        },
        'AVCC': {
            'in2_input': 3.264,
            'in2_min': 2.976,
            'in2_max': 3.632,
            'in2_alarm': 0.0,
            'in2_beep': 0.0
        },
        '+3.3V': {
            'in3_input': 3.264,
            'in3_min': 2.976,
            'in3_max': 3.632,
            'in3_alarm': 0.0,
            'in3_beep': 0.0
        },
        'in4': {
            'in4_input': 1.84,
            'in4_min': 0.0,
            'in4_max': 0.0,
            'in4_alarm': 1.0,
            'in4_beep': 0.0
        },
        'in5': {
            'in5_input': 0.92,
            'in5_min': 0.0,
            'in5_max': 0.0,
            'in5_alarm': 1.0,
            'in5_beep': 0.0
        },
        'in6': {
            'in6_input': 2.04,
            'in6_min': 0.0,
            'in6_max': 0.0,
            'in6_alarm': 1.0,
            'in6_beep': 0.0
        },
        '3VSB': {
            'in7_input': 3.392,
            'in7_min': 2.976,
            'in7_max': 3.632,
            'in7_alarm': 0.0,
            'in7_beep': 0.0
        },
        'Vbat': {
            'in8_input': 3.216,
            'in8_min': 2.704,
            'in8_max': 3.632,
            'in8_alarm': 0.0,
            'in8_beep': 0.0
        },
        'in9': {
            'in9_input': 0.0,
            'in9_min': 0.0,
            'in9_max': 0.0,
            'in9_alarm': 0.0,
            'in9_beep': 0.0
        },
        'in10': {
            'in10_input': 0.848,
            'in10_min': 0.0,
            'in10_max': 0.0,
            'in10_alarm': 1.0,
            'in10_beep': 0.0
        },
        'in11': {
            'in11_input': 2.04,
            'in11_min': 0.0,
            'in11_max': 0.0,
            'in11_alarm': 1.0,
            'in11_beep': 0.0
        },
        'in12': {
            'in12_input': 1.672,
            'in12_min': 0.0,
            'in12_max': 0.0,
            'in12_alarm': 1.0,
            'in12_beep': 0.0
        },
        'in13': {
            'in13_input': 0.92,
            'in13_min': 0.0,
            'in13_max': 0.0,
            'in13_alarm': 1.0,
            'in13_beep': 0.0
        },
        'in14': {
            'in14_input': 1.464,
            'in14_min': 0.0,
            'in14_max': 0.0,
            'in14_alarm': 1.0,
            'in14_beep': 0.0
        },
        'fan1': {
            'fan1_input': 0.0,
            'fan1_min': 0.0,
            'fan1_alarm': 0.0,
            'fan1_beep': 0.0,
            'fan1_pulses': 2.0
        },
        'fan2': {
            'fan2_input': 0.0,
            'fan2_min': 0.0,
            'fan2_alarm': 0.0,
            'fan2_beep': 0.0,
            'fan2_pulses': 2.0
        },
        'fan3': {
            'fan3_input': 0.0,
            'fan3_min': 0.0,
            'fan3_alarm': 0.0,
            'fan3_beep': 0.0,
            'fan3_pulses': 2.0
        },
        'fan4': {
            'fan4_input': 0.0,
            'fan4_min': 0.0,
            'fan4_alarm': 0.0,
            'fan4_beep': 0.0,
            'fan4_pulses': 2.0
        },
        'fan5': {
            'fan5_input': 0.0,
            'fan5_min': 0.0,
            'fan5_alarm': 0.0,
            'fan5_beep': 0.0,
            'fan5_pulses': 2.0
        },
        'SYSTIN': {
            'temp1_input': 37.0,
            'temp1_max': 0.0,
            'temp1_max_hyst': 0.0,
            'temp1_alarm': 1.0,
            'temp1_type': 4.0,
            'temp1_offset': 0.0,
            'temp1_beep': 0.0
        },
        'CPUTIN': {
            'temp2_input': 37.5,
            'temp2_max': 80.0,
            'temp2_max_hyst': 75.0,
            'temp2_alarm': 0.0,
            'temp2_type': 4.0,
            'temp2_offset': 0.0,
            'temp2_beep': 0.0
        },
        'AUXTIN0': {
            'temp3_input': -62.0,
            'temp3_type': 4.0,
            'temp3_offset': 0.0
        },
        'AUXTIN1': {
            'temp4_input': 34.0,
            'temp4_type': 4.0,
            'temp4_offset': 0.0
        },
        'AUXTIN2': {
            'temp5_input': -62.0,
            'temp5_type': 4.0,
            'temp5_offset': 0.0
        },
        'AUXTIN3': {
            'temp6_input': 42.0,
            'temp6_type': 4.0,
            'temp6_offset': 0.0
        },
        'PCH_CHIP_CPU_MAX_TEMP': {
            'temp7_input': 0.0
        },
        'PCH_CHIP_TEMP': {
            'temp8_input': 0.0
        },
        'PCH_CPU_TEMP': {
            'temp9_input': 0.0
        },
        'PCH_MCH_TEMP': {
            'temp10_input': 0.0
        },
        'TSI0_TEMP': {
            'temp11_input': 41.375
        },
        'intrusion0': {
            'intrusion0_alarm': 1.0,
            'intrusion0_beep': 0.0
        },
        'intrusion1': {
            'intrusion1_alarm': 1.0,
            'intrusion1_beep': 0.0
        },
        'beep_enable': {
            'beep_enable': 0.0
        }
    },
    'bnxt_en-pci-4201': {
        'Adapter': 'PCI adapter',
        'temp1': {
            'temp1_input': 43.0
        }
    }
}
