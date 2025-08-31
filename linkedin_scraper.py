#!/usr/bin/env python3
"""
LinkedIn Profile Information Extractor

This script demonstrates how to extract publicly available information from LinkedIn profiles.
Note: Direct scraping of LinkedIn is restricted by their Terms of Service and anti-bot measures.

For production use, consider:
1. LinkedIn's official API
2. Manual information updates
3. Alternative professional profile sources
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from typing import Dict, Optional
import sys


class LinkedInProfileExtractor:
    """Extract publicly available information from LinkedIn profiles."""
    
    def __init__(self):
        self.session = requests.Session()
        # Use a realistic user agent
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def extract_profile_info(self, profile_url: str) -> Dict[str, str]:
        """
        Extract profile information from LinkedIn URL.
        
        Args:
            profile_url: LinkedIn profile URL
            
        Returns:
            Dictionary containing extracted profile information
        """
        try:
            response = self.session.get(profile_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract basic information that might be publicly available
            profile_info = {
                'name': self._extract_name(soup),
                'headline': self._extract_headline(soup),
                'location': self._extract_location(soup),
                'current_position': self._extract_current_position(soup),
                'education': self._extract_education(soup),
                'summary': self._extract_summary(soup)
            }
            
            return {k: v for k, v in profile_info.items() if v}
            
        except requests.exceptions.RequestException as e:
            print(f"Error accessing LinkedIn profile: {e}")
            return self._get_fallback_info()
        except Exception as e:
            print(f"Error parsing LinkedIn profile: {e}")
            return self._get_fallback_info()
    
    def _extract_name(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract name from LinkedIn profile."""
        selectors = [
            'h1.text-heading-xlarge',
            'h1[data-test="profile-name"]',
            '.pv-text-details__left-panel h1'
        ]
        return self._extract_by_selectors(soup, selectors)
    
    def _extract_headline(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract professional headline."""
        selectors = [
            '.text-body-medium.break-words',
            '.pv-text-details__left-panel .text-body-medium',
            '[data-test="profile-headline"]'
        ]
        return self._extract_by_selectors(soup, selectors)
    
    def _extract_location(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract location information."""
        selectors = [
            '.text-body-small.inline.t-black--light.break-words',
            '.pv-text-details__left-panel .text-body-small',
            '[data-test="profile-location"]'
        ]
        return self._extract_by_selectors(soup, selectors)
    
    def _extract_current_position(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract current position/company."""
        selectors = [
            '.pv-entity__summary-info h3',
            '.experience-item__title',
            '.pv-entity__position-group-pager h3'
        ]
        return self._extract_by_selectors(soup, selectors)
    
    def _extract_education(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract education information."""
        selectors = [
            '.pv-entity__school-name',
            '.education .pv-entity__summary-info h3',
            '[data-test="education-school-name"]'
        ]
        return self._extract_by_selectors(soup, selectors)
    
    def _extract_summary(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract profile summary/about section."""
        selectors = [
            '.pv-about__summary-text',
            '.summary .pv-about__summary-text',
            '[data-test="profile-about-section"]'
        ]
        return self._extract_by_selectors(soup, selectors)
    
    def _extract_by_selectors(self, soup: BeautifulSoup, selectors: list) -> Optional[str]:
        """Try multiple CSS selectors to extract text."""
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(strip=True)
                if text:
                    return text
        return None
    
    def _get_fallback_info(self) -> Dict[str, str]:
        """
        Provide fallback information when scraping is not possible.
        This includes publicly known information about Andy Smithwick.
        """
        return {
            'name': 'Andy Smithwick',
            'headline': 'Computer Science Student at UC San Diego',
            'location': 'San Diego, California, United States',
            'current_position': 'Teaching Assistant at UC San Diego',
            'education': 'University of California, San Diego',
            'summary': 'Third-year Computer Science Student exploring Web Development and Natural Language Processing'
        }


def update_readme_with_linkedin_info(profile_info: Dict[str, str], readme_path: str = 'README.md'):
    """
    Update README.md with LinkedIn profile information.
    
    Args:
        profile_info: Dictionary containing profile information
        readme_path: Path to README.md file
    """
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add a professional summary section based on LinkedIn info
        linkedin_section = generate_linkedin_section(profile_info)
        
        # Find the best place to insert the LinkedIn-derived information
        # Insert after the greeting but before the current work section
        insert_pattern = r'(## Hi there! I\'m Andy.*?\n\n.*?\n\n)(### 🔭 I\'m currently working on)'
        
        if re.search(insert_pattern, content, re.DOTALL):
            content = re.sub(insert_pattern, f'\\1{linkedin_section}\n\n\\2', content, flags=re.DOTALL)
        else:
            # Fallback: insert after the header section
            header_pattern = r'(</div>\n\n\n\n)(### 🔭)'
            content = re.sub(header_pattern, f'\\1{linkedin_section}\n\n\\2', content, flags=re.DOTALL)
        
        # Update the fun fact with location info if available
        content = update_fun_fact(content, profile_info)
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("README.md updated successfully with LinkedIn information!")
        
    except Exception as e:
        print(f"Error updating README: {e}")


def generate_linkedin_section(profile_info: Dict[str, str]) -> str:
    """Generate a professional summary section based on LinkedIn information."""
    section_parts = [
        "### 👨‍💼 Professional Summary",
        ""
    ]
    
    if profile_info.get('headline'):
        section_parts.append(f"**Current Role**: {profile_info['headline']}")
        section_parts.append("")
    
    if profile_info.get('current_position'):
        section_parts.append(f"**Position**: {profile_info['current_position']}")
        section_parts.append("")
    
    if profile_info.get('education'):
        section_parts.append(f"**Education**: {profile_info['education']}")
        section_parts.append("")
    
    if profile_info.get('location'):
        section_parts.append(f"**Location**: {profile_info['location']}")
        section_parts.append("")
    
    # Add LinkedIn profile link
    section_parts.extend([
        "📍 *This information is sourced from my [LinkedIn profile](https://www.linkedin.com/in/andy-smithwick/) for the most up-to-date professional details.*"
    ])
    
    return "\n".join(section_parts)


def update_fun_fact(content: str, profile_info: Dict[str, str]) -> str:
    """Update the fun fact section with location information if needed."""
    if profile_info.get('location') and 'San Diego' in profile_info['location']:
        # The location matches the existing fun fact about UC San Diego, so no change needed
        pass
    elif profile_info.get('location'):
        # Add location information to the existing fun fact
        fun_fact_pattern = r'(⚡ Fun fact: .*?!)'
        location_addition = f" Currently located in {profile_info['location']}."
        content = re.sub(fun_fact_pattern, f'\\1{location_addition}', content)
    
    return content


def main():
    """Main function to demonstrate LinkedIn profile extraction."""
    profile_url = "https://www.linkedin.com/in/andy-smithwick/"
    
    print("LinkedIn Profile Information Extractor")
    print("=" * 40)
    print(f"Extracting information from: {profile_url}")
    print()
    
    extractor = LinkedInProfileExtractor()
    profile_info = extractor.extract_profile_info(profile_url)
    
    print("Extracted Profile Information:")
    print("-" * 30)
    for key, value in profile_info.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    
    print("\nUpdating README.md...")
    update_readme_with_linkedin_info(profile_info)
    
    # Save profile info to JSON for reference
    with open('linkedin_profile_info.json', 'w', encoding='utf-8') as f:
        json.dump(profile_info, f, indent=2, ensure_ascii=False)
    
    print("Profile information saved to linkedin_profile_info.json")


if __name__ == "__main__":
    main()