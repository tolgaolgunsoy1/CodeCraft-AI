import re
import os

class AICodeReviewer:
    """Static analysis and code quality checker"""
    
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.suggestions = []
    
    def review_kotlin_file(self, file_path, content):
        """Review Kotlin code for common issues"""
        self.issues = []
        self.warnings = []
        self.suggestions = []
        
        self._check_memory_leaks(content)
        self._check_coroutines(content)
        self._check_null_safety(content)
        self._check_resource_management(content)
        self._check_performance(content)
        
        return {
            'file': file_path,
            'issues': self.issues,
            'warnings': self.warnings,
            'suggestions': self.suggestions,
            'score': self._calculate_score()
        }
    
    def _check_memory_leaks(self, content):
        """Check for potential memory leaks"""
        # Context leaks
        if re.search(r'companion object.*Context', content):
            self.issues.append({
                'type': 'MEMORY_LEAK',
                'severity': 'HIGH',
                'message': 'Context stored in companion object causes memory leak',
                'fix': 'Use Application context or WeakReference'
            })
        
        # Handler without WeakReference
        if 'Handler(' in content and 'WeakReference' not in content:
            self.warnings.append({
                'type': 'POTENTIAL_LEAK',
                'severity': 'MEDIUM',
                'message': 'Handler without WeakReference may cause leak',
                'fix': 'Use WeakReference<Activity> or lifecycle-aware components'
            })
    
    def _check_coroutines(self, content):
        """Check coroutine usage"""
        # Network calls without coroutines
        if 'Retrofit' in content or 'OkHttp' in content:
            if 'suspend' not in content and 'viewModelScope' not in content:
                self.issues.append({
                    'type': 'BLOCKING_CALL',
                    'severity': 'HIGH',
                    'message': 'Network call not in coroutine - blocks UI thread',
                    'fix': 'Use suspend function with viewModelScope.launch'
                })
        
        # GlobalScope usage
        if 'GlobalScope.launch' in content:
            self.warnings.append({
                'type': 'BAD_PRACTICE',
                'severity': 'MEDIUM',
                'message': 'GlobalScope.launch is not lifecycle-aware',
                'fix': 'Use viewModelScope or lifecycleScope'
            })
    
    def _check_null_safety(self, content):
        """Check null safety"""
        # Force unwrap
        force_unwraps = len(re.findall(r'!!', content))
        if force_unwraps > 3:
            self.warnings.append({
                'type': 'NULL_SAFETY',
                'severity': 'MEDIUM',
                'message': f'Too many force unwraps (!!): {force_unwraps} occurrences',
                'fix': 'Use safe calls (?.) or let/apply blocks'
            })
    
    def _check_resource_management(self, content):
        """Check resource management"""
        # Unclosed resources
        if 'FileInputStream' in content or 'FileOutputStream' in content:
            if '.use {' not in content:
                self.issues.append({
                    'type': 'RESOURCE_LEAK',
                    'severity': 'HIGH',
                    'message': 'File stream not properly closed',
                    'fix': 'Use .use {} block for automatic closing'
                })
    
    def _check_performance(self, content):
        """Check performance issues"""
        # findViewById in loops
        if 'for' in content and 'findViewById' in content:
            self.warnings.append({
                'type': 'PERFORMANCE',
                'severity': 'MEDIUM',
                'message': 'findViewById in loop - performance issue',
                'fix': 'Use ViewBinding or cache view references'
            })
        
        # String concatenation in loops
        if re.search(r'for.*\+.*String', content):
            self.suggestions.append({
                'type': 'OPTIMIZATION',
                'severity': 'LOW',
                'message': 'String concatenation in loop',
                'fix': 'Use StringBuilder for better performance'
            })
    
    def _calculate_score(self):
        """Calculate code quality score"""
        score = 100
        score -= len(self.issues) * 10
        score -= len(self.warnings) * 5
        score -= len(self.suggestions) * 2
        return max(0, score)
    
    def generate_report(self, reviews):
        """Generate markdown report"""
        report = "# 🔍 Code Review Report\n\n"
        
        total_issues = sum(len(r['issues']) for r in reviews)
        total_warnings = sum(len(r['warnings']) for r in reviews)
        avg_score = sum(r['score'] for r in reviews) / len(reviews) if reviews else 0
        
        report += f"## 📊 Summary\n\n"
        report += f"- **Files Reviewed:** {len(reviews)}\n"
        report += f"- **Issues:** {total_issues}\n"
        report += f"- **Warnings:** {total_warnings}\n"
        report += f"- **Average Score:** {avg_score:.1f}/100\n\n"
        
        for review in reviews:
            if review['issues'] or review['warnings']:
                report += f"### 📄 {os.path.basename(review['file'])}\n\n"
                report += f"**Score:** {review['score']}/100\n\n"
                
                if review['issues']:
                    report += "#### ❌ Issues\n\n"
                    for issue in review['issues']:
                        report += f"- **{issue['type']}** ({issue['severity']})\n"
                        report += f"  - {issue['message']}\n"
                        report += f"  - Fix: {issue['fix']}\n\n"
                
                if review['warnings']:
                    report += "#### ⚠️ Warnings\n\n"
                    for warning in review['warnings']:
                        report += f"- **{warning['type']}** ({warning['severity']})\n"
                        report += f"  - {warning['message']}\n"
                        report += f"  - Fix: {warning['fix']}\n\n"
        
        return report
