#!/usr/bin/env python3
"""
AGen_UI - UI Development & Branding Agent
Handles frontend styling and ENKI AGENTIC branding
"""

import json
import os
from datetime import datetime

class AGen_UI:
    def __init__(self):
        self.project_dir = '/home/ubuntu/enki-agentic/ui-design'
        self.brand_dir = f'{self.project_dir}/branding'
        self.init_directories()
        
    def init_directories(self):
        os.makedirs(f'{self.brand_dir}/logos', exist_ok=True)
        os.makedirs(f'{self.brand_dir}/colors', exist_ok=True)
        os.makedirs(f'{self.brand_dir}/typography', exist_ok=True)
        os.makedirs(f'{self.brand_dir}/guidelines', exist_ok=True)
        
    def generate_brand_strategy(self):
        strategy = {
            'company_name': 'ENKI AGENTIC',
            'tagline': 'We Bring The ME',
            'positioning': 'First-mover AI agent solution provider for NZ mega industries',
            'namesake': 'ENKI - Sumerian god of wisdom, creation, intelligence',
            'mission': 'Bring the divine powers (ME) of the digital age to humanity'
        }
        
        with open(f'{self.brand_dir}/brand_strategy.json', 'w') as f:
            json.dump(strategy, f, indent=2)
        return strategy
    
    def generate_color_palette(self):
        palette = {
            'primary': {
                'enki_blue': '#0066FF',
                'enki_gold': '#FFD700'
            },
            'secondary': {
                'deep_navy': '#0A1929',
                'electric_cyan': '#00D9FF',
                'alert_red': '#FF3366'
            },
            'neutrals': {
                'pure_white': '#FFFFFF',
                'soft_gray': '#F5F7FA',
                'medium_gray': '#8B9AAF',
                'dark_gray': '#2D3748'
            }
        }
        
        with open(f'{self.brand_dir}/colors/palette.json', 'w') as f:
            json.dump(palette, f, indent=2)
            
        # CSS variables
        css = ''':root {
  --enki-blue: #0066FF;
  --enki-gold: #FFD700;
  --deep-navy: #0A1929;
  --electric-cyan: #00D9FF;
  --alert-red: #FF3366;
  --pure-white: #FFFFFF;
  --soft-gray: #F5F7FA;
}'''
        with open(f'{self.brand_dir}/colors/variables.css', 'w') as f:
            f.write(css)
            
        return palette
    
    def generate_frontend_css(self):
        css = '''/* ENKI AGENTIC - Frontend Styling */

/* Agent Card */
.agent-card {
  background: linear-gradient(135deg, #0A1929 0%, #1A2B3C 100%);
  border: 1px solid rgba(0, 217, 255, 0.2);
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 102, 255, 0.15);
  transition: all 0.3s ease;
}

.agent-card:hover {
  border-color: #00D9FF;
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0, 102, 255, 0.25);
}

/* Status Indicators */
.status-active {
  color: #00D9FF;
  animation: pulse 2s infinite;
}

.status-warning {
  color: #FFD700;
}

.status-critical {
  color: #FF3366;
  animation: flash 1s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

@keyframes flash {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

/* Primary Button */
.btn-primary {
  background: linear-gradient(135deg, #0066FF 0%, #00D9FF 100%);
  color: #FFFFFF;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 14px rgba(0, 102, 255, 0.4);
}

.btn-primary:hover {
  filter: brightness(1.1);
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(0, 102, 255, 0.5);
}

/* Data Display */
.data-card {
  background: #F5F7FA;
  border-radius: 12px;
  padding: 24px;
  border-left: 4px solid #0066FF;
}

.metric-value {
  font-size: 36px;
  font-weight: 700;
  color: #0066FF;
}

.metric-label {
  font-size: 14px;
  color: #8B9AAF;
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* Dashboard Header */
.dashboard-header {
  background: linear-gradient(135deg, #0A1929 0%, #0D2137 100%);
  padding: 24px 32px;
  border-bottom: 2px solid rgba(0, 217, 255, 0.3);
}

.brand-title {
  font-size: 28px;
  font-weight: 700;
  color: #FFFFFF;
  letter-spacing: 2px;
}

.brand-title span {
  color: #FFD700;
}

/* Hot Lead Alert */
.hot-lead-alert {
  background: linear-gradient(135deg, #FF3366 0%, #FF6B6B 100%);
  color: #FFFFFF;
  padding: 16px 24px;
  border-radius: 8px;
  font-weight: 600;
  animation: slideIn 0.5s ease;
}

@keyframes slideIn {
  from { transform: translateX(-100%); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}
'''
        with open(f'{self.project_dir}/components/enki-theme.css', 'w') as f:
            f.write(css)
        return 'CSS generated'
    
    def generate_all(self):
        print('AGen_UI - Generating ENKI Branding...')
        self.generate_brand_strategy()
        print('✓ Brand strategy created')
        self.generate_color_palette()
        print('✓ Color palette created')
        self.generate_frontend_css()
        print('✓ Frontend CSS created')
        print('\nAGen_UI branding complete!')
        return {'status': 'complete'}

if __name__ == '__main__':
    import sys
    ui = AGen_UI()
    if len(sys.argv) > 1 and sys.argv[1] == 'generate-all':
        ui.generate_all()
    else:
        print('AGen_UI - ENKI Branding Agent')
        print('Usage: python3 agen_ui.py generate-all')
