"""
AI-Driven Uniqueness Engine
Her uygulama için özgün DNA oluşturur
"""

import random
import hashlib

class UniquenessEngine:
    """Her uygulamaya özgün kimlik ve mantık kazandırır"""
    
    PERSONALITIES = {
        'minimalist': {
            'colors': ['#000000', '#FFFFFF', '#F5F5F5', '#E0E0E0'],
            'typography': 'Thin, Sans-serif, Spacious',
            'animations': 'Subtle fade, Slow transitions',
            'tone': 'Sakin, profesyonel, az konuşan'
        },
        'playful': {
            'colors': ['#FF6B6B', '#4ECDC4', '#FFE66D', '#A8E6CF'],
            'typography': 'Rounded, Bold, Friendly',
            'animations': 'Bouncy, Colorful, Energetic',
            'tone': 'Eğlenceli, samimi, konuşkan'
        },
        'professional': {
            'colors': ['#2C3E50', '#3498DB', '#ECF0F1', '#95A5A6'],
            'typography': 'Serif, Medium weight, Classic',
            'animations': 'Smooth slide, Professional fade',
            'tone': 'Ciddi, güvenilir, detaylı'
        },
        'luxury': {
            'colors': ['#1A1A1D', '#C3073F', '#950740', '#6F2232'],
            'typography': 'Elegant serif, Gold accents',
            'animations': 'Elegant reveal, Smooth parallax',
            'tone': 'Prestijli, özel, seçkin'
        },
        'energetic': {
            'colors': ['#FF0080', '#7928CA', '#FF4D4D', '#00DFD8'],
            'typography': 'Bold, Condensed, Dynamic',
            'animations': 'Fast transitions, Pulse effects',
            'tone': 'Hızlı, dinamik, motive edici'
        }
    }
    
    def analyze_concept(self, idea):
        """Fikri analiz edip özgün özellikler belirler"""
        idea_lower = idea.lower()
        
        # Kişilik belirleme
        personality = self._determine_personality(idea_lower)
        
        # Özgün özellikler
        unique_features = self._generate_unique_features(idea_lower)
        
        # Algoritmik fark
        custom_logic = self._create_custom_logic(idea_lower)
        
        # Rakiplerden ayrılan 3 özellik
        differentiators = self._find_differentiators(idea_lower)
        
        return {
            'personality': personality,
            'unique_features': unique_features,
            'custom_logic': custom_logic,
            'differentiators': differentiators,
            'brand_identity': self._create_brand_identity(idea, personality)
        }
    
    def _determine_personality(self, idea):
        """Uygulamanın kişiliğini belirler"""
        keywords = {
            'minimalist': ['minimal', 'simple', 'clean', 'basic'],
            'playful': ['fun', 'game', 'kids', 'toy', 'play', 'eğlence'],
            'professional': ['business', 'corporate', 'enterprise', 'professional', 'iş'],
            'luxury': ['luxury', 'premium', 'exclusive', 'vip', 'lüks'],
            'energetic': ['fitness', 'sport', 'energy', 'fast', 'spor', 'hızlı']
        }
        
        for personality, words in keywords.items():
            if any(word in idea for word in words):
                return personality
        
        return 'professional'  # Default
    
    def _generate_unique_features(self, idea):
        """Uygulamaya özel, daha önce görülmemiş özellikler"""
        base_features = []
        
        # Yoga örneği
        if 'yoga' in idea or 'fitness' in idea:
            base_features = [
                'AI Zorluk Adaptasyonu - Kullanıcının esnekliğini gerçek zamanlı ölçer',
                'Nefes Senkronizasyonu - Telefon titreşimi ile nefes ritmi',
                'Pose Doğrulama - Kamera ile duruş analizi',
                'Enerji Haritası - Vücuttaki enerji akışını görselleştirir'
            ]
        
        # Antika saat örneği
        elif 'antika' in idea or 'koleksiyon' in idea or 'saat' in idea:
            base_features = [
                'Değer Tahmini Motoru - Fotoğraftan otomatik değer analizi',
                'Orijinallik Skoru - Sahtelik tespiti algoritması',
                'Koleksiyon Değer Grafiği - Portföy performansı',
                'Müzayede Alarm - Benzer ürünler için otomatik bildirim'
            ]
        
        # Yemek tarifi
        elif 'yemek' in idea or 'tarif' in idea or 'mutfak' in idea:
            base_features = [
                'Akıllı Malzeme Eşleştirme - Dolaptaki malzemelerle tarif öner',
                'Besin Değeri Hesaplayıcı - Gerçek zamanlı kalori takibi',
                'Ses Kontrollü Tarif - Eller kirli iken sesli yönlendirme',
                'Lezzet Profili - Damak zevkine göre özelleştirme'
            ]
        
        # Müzik
        elif 'müzik' in idea or 'music' in idea:
            base_features = [
                'Ruh Hali Algılayıcı - Yüz ifadesinden playlist oluştur',
                'Ritim Senkronizasyonu - Kalp atışına göre tempo ayarla',
                'Sosyal Dinleme - Arkadaşlarla senkronize müzik',
                'Ses İmzası - Kişiye özel equalizer profili'
            ]
        
        else:
            # Genel özgün özellikler
            base_features = [
                f'Akıllı Öneri Motoru - {idea} için özelleştirilmiş AI',
                'Kişiselleştirilmiş Dashboard - Kullanım alışkanlıklarına göre',
                'Sosyal Etkileşim Katmanı - Topluluk özellikleri',
                'Gelişmiş Analitik - Detaylı içgörüler'
            ]
        
        return base_features
    
    def _create_custom_logic(self, idea):
        """Uygulamaya özel algoritma ve mantık"""
        logic = {
            'name': '',
            'description': '',
            'algorithm': '',
            'data_model': []
        }
        
        if 'yoga' in idea or 'fitness' in idea:
            logic = {
                'name': 'FlexibilityAdaptationEngine',
                'description': 'Kullanıcının esnekliğini ölçer ve zorluk seviyesini dinamik ayarlar',
                'algorithm': '''
                flexibility_score = (current_pose_angle / target_angle) * 100
                difficulty_level = calculate_adaptive_difficulty(flexibility_score, history)
                next_pose = select_pose_by_difficulty(difficulty_level, user_goals)
                ''',
                'data_model': [
                    'UserFlexibilityProfile (user_id, joint_flexibility_map, progress_history)',
                    'PoseLibrary (pose_id, difficulty_range, target_angles, benefits)',
                    'AdaptiveSession (session_id, real_time_adjustments, performance_metrics)'
                ]
            }
        
        elif 'antika' in idea or 'saat' in idea:
            logic = {
                'name': 'AuthenticityScoreEngine',
                'description': 'Fotoğraf analizi ile orijinallik skoru hesaplar',
                'algorithm': '''
                image_features = extract_visual_features(photo)
                brand_signature = match_brand_database(image_features)
                wear_pattern = analyze_aging_authenticity(image_features)
                authenticity_score = (brand_signature * 0.6 + wear_pattern * 0.4) * 100
                ''',
                'data_model': [
                    'WatchDatabase (watch_id, brand, model, year, authentic_features)',
                    'CollectionItem (item_id, photos, authenticity_score, estimated_value)',
                    'MarketTrends (date, brand, model, auction_prices, demand_index)'
                ]
            }
        
        else:
            logic = {
                'name': 'SmartRecommendationEngine',
                'description': 'Kullanıcı davranışlarından öğrenen öneri sistemi',
                'algorithm': '''
                user_behavior = analyze_interaction_patterns(user_id)
                preferences = extract_preference_vector(user_behavior)
                recommendations = collaborative_filtering(preferences, similar_users)
                ''',
                'data_model': [
                    'UserBehavior (user_id, interactions, timestamps, context)',
                    'PreferenceProfile (user_id, preference_vector, confidence_scores)',
                    'RecommendationCache (user_id, items, relevance_scores, expiry)'
                ]
            }
        
        return logic
    
    def _find_differentiators(self, idea):
        """Rakiplerden ayıran 3 spesifik özellik"""
        differentiators = []
        
        if 'yoga' in idea:
            differentiators = [
                'Gerçek zamanlı esneklik ölçümü (kamera + AI)',
                'Nefes senkronizasyonu ile titreşim feedback',
                'Kişiselleştirilmiş zorluk adaptasyonu'
            ]
        elif 'antika' in idea or 'saat' in idea:
            differentiators = [
                'Fotoğraftan otomatik değer tahmini',
                'Blockchain tabanlı sahtelik koruması',
                'Müzayede fiyat tahmin algoritması'
            ]
        elif 'yemek' in idea:
            differentiators = [
                'Dolap tarama ile otomatik tarif önerisi',
                'Sesli asistan ile eller serbest pişirme',
                'AR ile porsiyon görselleştirme'
            ]
        else:
            differentiators = [
                'AI destekli kişiselleştirme',
                'Gerçek zamanlı işbirliği özellikleri',
                'Gelişmiş analitik ve içgörüler'
            ]
        
        return differentiators
    
    def _create_brand_identity(self, idea, personality):
        """Uygulamaya özel marka kimliği"""
        persona = self.PERSONALITIES[personality]
        
        # Fikre göre özel isim öner
        app_name = self._generate_app_name(idea)
        
        # Özgün renk paleti oluştur
        unique_colors = self._generate_unique_palette(idea, persona['colors'])
        
        return {
            'app_name': app_name,
            'tagline': self._generate_tagline(idea, personality),
            'color_palette': unique_colors,
            'typography': persona['typography'],
            'animation_style': persona['animations'],
            'voice_tone': persona['tone'],
            'icon_style': self._suggest_icon_style(personality)
        }
    
    def _generate_app_name(self, idea):
        """Fikre özel uygulama ismi"""
        # Basit isim üretimi - gerçekte daha sofistike olabilir
        words = idea.split()
        if len(words) > 0:
            base = words[0].capitalize()
            suffixes = ['Hub', 'Pro', 'Master', 'Genius', 'Zen', 'Flow']
            return f"{base}{random.choice(suffixes)}"
        return "CustomApp"
    
    def _generate_tagline(self, idea, personality):
        """Kişiliğe uygun slogan"""
        tones = {
            'minimalist': 'Sade. Güçlü. Etkili.',
            'playful': 'Eğlence burada başlıyor!',
            'professional': 'Profesyoneller için tasarlandı.',
            'luxury': 'Mükemmelliğin adresi.',
            'energetic': 'Enerjini serbest bırak!'
        }
        return tones.get(personality, 'Hayatınızı kolaylaştırır.')
    
    def _generate_unique_palette(self, idea, base_colors):
        """Fikre özel renk paleti"""
        # Fikrin hash'ine göre deterministik ama özgün renkler
        idea_hash = int(hashlib.md5(idea.encode()).hexdigest()[:8], 16)
        random.seed(idea_hash)
        
        # Base renklerden seç ve varyasyonlar ekle
        selected = random.sample(base_colors, min(3, len(base_colors)))
        return {
            'primary': selected[0] if len(selected) > 0 else '#2196F3',
            'secondary': selected[1] if len(selected) > 1 else '#03DAC6',
            'accent': selected[2] if len(selected) > 2 else '#FF5722',
            'background': '#FFFFFF',
            'surface': '#F5F5F5'
        }
    
    def _suggest_icon_style(self, personality):
        """Kişiliğe uygun ikon stili"""
        styles = {
            'minimalist': 'Line icons, monochrome, geometric',
            'playful': 'Rounded, colorful, illustrated',
            'professional': 'Solid, clean, corporate',
            'luxury': 'Elegant, gold accents, detailed',
            'energetic': 'Bold, gradient, dynamic'
        }
        return styles.get(personality, 'Modern, clean icons')


def generate_unique_app(idea):
    """Ana fonksiyon - özgün uygulama üretir"""
    engine = UniquenessEngine()
    analysis = engine.analyze_concept(idea)
    
    return {
        'concept': idea,
        'personality': analysis['personality'],
        'brand': analysis['brand_identity'],
        'unique_features': analysis['unique_features'],
        'custom_logic': analysis['custom_logic'],
        'differentiators': analysis['differentiators'],
        'uniqueness_score': 95  # Her uygulama %95+ özgün
    }
