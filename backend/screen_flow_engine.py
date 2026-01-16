"""
Screen Flow Engine - Professional App Structure
"""

class ScreenFlowEngine:
    
    SCREEN_FLOWS = {
        'ecommerce': {
            'screens': [
                {'name': 'SplashActivity', 'type': 'splash', 'duration': 2},
                {'name': 'OnboardingActivity', 'type': 'onboarding', 'slides': 3},
                {'name': 'LoginActivity', 'type': 'auth', 'social': True},
                {'name': 'MainActivity', 'type': 'dashboard', 'layout': 'grid'},
                {'name': 'ProductDetailActivity', 'type': 'detail'},
                {'name': 'CartActivity', 'type': 'cart'},
                {'name': 'CheckoutActivity', 'type': 'checkout'},
                {'name': 'OrderHistoryActivity', 'type': 'list'},
                {'name': 'ProfileActivity', 'type': 'profile'},
                {'name': 'SettingsActivity', 'type': 'settings'}
            ],
            'navigation': 'bottom'
        },
        'social_media': {
            'screens': [
                {'name': 'SplashActivity', 'type': 'splash', 'duration': 1.5},
                {'name': 'OnboardingActivity', 'type': 'onboarding', 'slides': 4},
                {'name': 'LoginActivity', 'type': 'auth', 'social': True},
                {'name': 'MainActivity', 'type': 'dashboard', 'layout': 'feed'},
                {'name': 'PostDetailActivity', 'type': 'detail'},
                {'name': 'CreatePostActivity', 'type': 'create'},
                {'name': 'NotificationsActivity', 'type': 'notifications'},
                {'name': 'ProfileActivity', 'type': 'profile'},
                {'name': 'SearchActivity', 'type': 'search'},
                {'name': 'SettingsActivity', 'type': 'settings'}
            ],
            'navigation': 'bottom'
        },
        'productivity': {
            'screens': [
                {'name': 'SplashActivity', 'type': 'splash', 'duration': 1},
                {'name': 'OnboardingActivity', 'type': 'onboarding', 'slides': 3},
                {'name': 'MainActivity', 'type': 'dashboard', 'layout': 'mixed'},
                {'name': 'TaskDetailActivity', 'type': 'detail'},
                {'name': 'CreateTaskActivity', 'type': 'create'},
                {'name': 'CalendarActivity', 'type': 'calendar'},
                {'name': 'StatisticsActivity', 'type': 'stats'},
                {'name': 'ProfileActivity', 'type': 'profile'},
                {'name': 'SettingsActivity', 'type': 'settings'}
            ],
            'navigation': 'drawer'
        },
        'health': {
            'screens': [
                {'name': 'SplashActivity', 'type': 'splash', 'duration': 1.5},
                {'name': 'OnboardingActivity', 'type': 'onboarding', 'slides': 4},
                {'name': 'LoginActivity', 'type': 'auth', 'social': False},
                {'name': 'MainActivity', 'type': 'dashboard', 'layout': 'cards'},
                {'name': 'WorkoutDetailActivity', 'type': 'detail'},
                {'name': 'TrackingActivity', 'type': 'tracking'},
                {'name': 'ProgressActivity', 'type': 'stats'},
                {'name': 'ProfileActivity', 'type': 'profile'},
                {'name': 'SettingsActivity', 'type': 'settings'}
            ],
            'navigation': 'tabs'
        },
        'news': {
            'screens': [
                {'name': 'SplashActivity', 'type': 'splash', 'duration': 1},
                {'name': 'MainActivity', 'type': 'dashboard', 'layout': 'list'},
                {'name': 'ArticleDetailActivity', 'type': 'detail'},
                {'name': 'CategoriesActivity', 'type': 'categories'},
                {'name': 'SearchActivity', 'type': 'search'},
                {'name': 'BookmarksActivity', 'type': 'bookmarks'},
                {'name': 'SettingsActivity', 'type': 'settings'}
            ],
            'navigation': 'drawer'
        },
        'default': {
            'screens': [
                {'name': 'SplashActivity', 'type': 'splash', 'duration': 1.5},
                {'name': 'OnboardingActivity', 'type': 'onboarding', 'slides': 3},
                {'name': 'MainActivity', 'type': 'dashboard', 'layout': 'mixed'},
                {'name': 'DetailActivity', 'type': 'detail'},
                {'name': 'ProfileActivity', 'type': 'profile'},
                {'name': 'SettingsActivity', 'type': 'settings'}
            ],
            'navigation': 'bottom'
        }
    }
    
    @staticmethod
    def get_screen_flow(category):
        """Get appropriate screen flow for app category"""
        category_lower = category.lower()
        
        if 'shop' in category_lower or 'store' in category_lower or 'commerce' in category_lower:
            return ScreenFlowEngine.SCREEN_FLOWS['ecommerce']
        elif 'social' in category_lower or 'chat' in category_lower or 'post' in category_lower:
            return ScreenFlowEngine.SCREEN_FLOWS['social_media']
        elif 'task' in category_lower or 'todo' in category_lower or 'productivity' in category_lower:
            return ScreenFlowEngine.SCREEN_FLOWS['productivity']
        elif 'health' in category_lower or 'fitness' in category_lower or 'workout' in category_lower:
            return ScreenFlowEngine.SCREEN_FLOWS['health']
        elif 'news' in category_lower or 'blog' in category_lower or 'article' in category_lower:
            return ScreenFlowEngine.SCREEN_FLOWS['news']
        else:
            return ScreenFlowEngine.SCREEN_FLOWS['default']
    
    @staticmethod
    def generate_activity_list(category):
        """Generate list of activities for manifest"""
        flow = ScreenFlowEngine.get_screen_flow(category)
        return [screen['name'] for screen in flow['screens']]
