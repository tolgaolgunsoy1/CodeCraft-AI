"""
Design Variation Engine - Her Proje İçin Özgün Tasarım
"""
import random

class DesignEngine:
    
    DESIGN_STYLES = {
        'neumorphism': {
            'elevation': '8dp',
            'corner_radius': '24dp',
            'shadow_color': '#40000000',
            'background': '#E0E5EC'
        },
        'glassmorphism': {
            'elevation': '0dp',
            'corner_radius': '16dp',
            'alpha': '0.7',
            'blur': '10dp',
            'background': '#80FFFFFF'
        },
        'material3': {
            'elevation': '4dp',
            'corner_radius': '12dp',
            'background': '#FFFFFF'
        },
        'flat': {
            'elevation': '0dp',
            'corner_radius': '8dp',
            'background': '#F5F5F5'
        }
    }
    
    COLOR_PALETTES = {
        'ocean': {'primary': '#006494', 'secondary': '#13293D', 'accent': '#247BA0', 'surface': '#E8F1F2'},
        'sunset': {'primary': '#FF6B35', 'secondary': '#F7931E', 'accent': '#C1292E', 'surface': '#FFF8F0'},
        'forest': {'primary': '#2D6A4F', 'secondary': '#40916C', 'accent': '#52B788', 'surface': '#D8F3DC'},
        'lavender': {'primary': '#7209B7', 'secondary': '#560BAD', 'accent': '#B5179E', 'surface': '#F0E6FF'},
        'corporate': {'primary': '#1E3A8A', 'secondary': '#3B82F6', 'accent': '#60A5FA', 'surface': '#EFF6FF'},
        'warm': {'primary': '#DC2626', 'secondary': '#F59E0B', 'accent': '#FBBF24', 'surface': '#FEF3C7'},
        'cool': {'primary': '#0891B2', 'secondary': '#06B6D4', 'accent': '#22D3EE', 'surface': '#CFFAFE'},
        'elegant': {'primary': '#1F2937', 'secondary': '#4B5563', 'accent': '#9CA3AF', 'surface': '#F9FAFB'}
    }
    
    NAVIGATION_TYPES = ['bottom', 'drawer', 'tabs']
    
    DASHBOARD_LAYOUTS = ['grid', 'list', 'cards', 'mixed']
    
    @staticmethod
    def generate_unique_design(category='general'):
        """Generate unique design configuration for each project"""
        
        # Select style based on category
        if category in ['fintech', 'banking', 'finance']:
            style = random.choice(['glassmorphism', 'material3'])
            palette = random.choice(['corporate', 'elegant', 'cool'])
        elif category in ['education', 'learning', 'kids']:
            style = random.choice(['flat', 'material3'])
            palette = random.choice(['warm', 'lavender', 'sunset'])
        elif category in ['health', 'fitness', 'wellness']:
            style = random.choice(['neumorphism', 'material3'])
            palette = random.choice(['forest', 'ocean', 'cool'])
        else:
            style = random.choice(list(DesignEngine.DESIGN_STYLES.keys()))
            palette = random.choice(list(DesignEngine.COLOR_PALETTES.keys()))
        
        return {
            'style': style,
            'style_config': DesignEngine.DESIGN_STYLES[style],
            'palette': palette,
            'colors': DesignEngine.COLOR_PALETTES[palette],
            'navigation': random.choice(DesignEngine.NAVIGATION_TYPES),
            'dashboard_layout': random.choice(DesignEngine.DASHBOARD_LAYOUTS),
            'onboarding_style': random.choice(['slides', 'minimal', 'animated']),
            'splash_style': random.choice(['logo', 'brand', 'gradient'])
        }
    
    @staticmethod
    def generate_colors_xml(design):
        """Generate colors.xml with unique palette"""
        colors = design['colors']
        return f'''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="primary">{colors['primary']}</color>
    <color name="secondary">{colors['secondary']}</color>
    <color name="accent">{colors['accent']}</color>
    <color name="surface">{colors['surface']}</color>
    <color name="background">#FFFFFF</color>
    <color name="error">#DC2626</color>
</resources>'''
    
    @staticmethod
    def generate_themes_xml(design):
        """Generate themes.xml with unique style"""
        style_config = design['style_config']
        return f'''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="AppTheme" parent="Theme.Material3.DayNight">
        <item name="colorPrimary">@color/primary</item>
        <item name="colorSecondary">@color/secondary</item>
        <item name="colorSurface">@color/surface</item>
        <item name="shapeAppearanceSmallComponent">@style/ShapeAppearance.App.SmallComponent</item>
        <item name="shapeAppearanceMediumComponent">@style/ShapeAppearance.App.MediumComponent</item>
    </style>
    
    <style name="ShapeAppearance.App.SmallComponent" parent="">
        <item name="cornerFamily">rounded</item>
        <item name="cornerSize">{style_config['corner_radius']}</item>
    </style>
    
    <style name="ShapeAppearance.App.MediumComponent" parent="">
        <item name="cornerFamily">rounded</item>
        <item name="cornerSize">{style_config['corner_radius']}</item>
    </style>
    
    <style name="CardStyle">
        <item name="cardElevation">{style_config['elevation']}</item>
        <item name="cardCornerRadius">{style_config['corner_radius']}</item>
        <item name="cardBackgroundColor">{style_config['background']}</item>
    </style>
</resources>'''
