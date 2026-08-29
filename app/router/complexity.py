import os

class ComplexityAnalyzer:

    TIER_2_KEYWORDS = [
        "summarize",
        "summary",
        "classify",
        "classification",
        "analyze",
        "analysis",
        "compare",
        "explain",
        "evaluate",
        "sentiment",
        "categorize",
        "organize"
    ]

    TIER_3_KEYWORDS = [
        "design",
        "architecture",
        "architect",
        "multi-step",
        "reasoning",
        "reason step by step",
        "step by step",
        "tradeoff",
        "tradeoffs",
        "recommend",
        "strategy",
        "strategic",
        "nuanced",
        "complex",
        "distributed",
        "system design",
        "solve"
    ]

    def analyze(self, prompt: str) -> str:
        """
        Returns:
            tier_1
            tier_2
            tier_3
        """

        normalized_prompt = prompt.lower().strip()
        score = self._calculate_score(
            normalized_prompt
        )

        if score >= 6:
            return "tier_3"
        elif score >= 3:
            return "tier_2"
        
        return "tier_1"
    
    def _calculate_score(self, prompt: str) -> int:
        score = 0

        word_count = len(prompt.split())

        if word_count > 300:
            score += 3
        elif word_count > 100:
            score += 2
        elif word_count > 40:
            score += 1
        

        tier_2_matches = self._count_keywords(
            prompt,
            self.TIER_2_KEYWORDS
        )

        score += min(tier_2_matches, 2)

        tier_3_matches = self._count_keywords(
            prompt,
            self.TIER_3_KEYWORDS
        )

        score += tier_3_matches * 3
        

    def _count_keywords(self, text: str, keywords: list[str]) -> int:
        count = 0

        for keyword in keywords:
            if keyword in text:
                count+=1
        return count