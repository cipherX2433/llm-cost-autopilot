import re
from app.models.routing import ComplexityResult

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

    CONSTRAINT_KEYWORDS = [
        "must",
        "should",
        "only",
        "at least",
        "at most",
        "do not",
        "don't",
        "ensure",
        "requirement"
    ]

    def analyze(self, prompt: str) -> ComplexityResult:

        normalized_prompt = prompt.lower().strip()

        score = 0
        reason = []

        # Propmt length
        word_count = len(normalized_prompt.split())

        if word_count > 300:
            score += 3

            reason.append(
                "Very long prompt"
            )
        elif word_count > 100:
            score += 2

            reason.append(
                "Long prompt"
            )
        elif word_count > 40:
            score += 1

            reason.append(
                "Moderate prompt length"
            )
        
        #FIND KEYWORDS FOR TIER-2
        tier_2_matches = self._find_keywords(
            normalized_prompt,
            self.TIER_2_KEYWORDS
        )

        # SCORE CAL FOR TIER-2
        if tier_2_matches:

            keyword_score = min(len(tier_2_matches), 2)
            score += keyword_score
            reason.append(
                "Moderate task keywords: " + ", ".join(tier_2_matches)
            )
        
        #FOR TIER-3
        tier_3_matches = self._find_keywords(
            normalized_prompt,
            self.TIER_3_KEYWORDS
        )

        if tier_3_matches:
            
            keyword_score = (len(tier_3_matches) * 3)
            score += keyword_score

            reason.append(
                "Complex task keyword: " + ", ".join(tier_3_matches)
            )
    
        # Numbered instruction
        numbered_steps = len(
            re.findall(
                r"\d+\.",
                normalized_prompt
            )
        )

        if numbered_steps >= 3:

            score += 2

            reason.append(
                f"{numbered_steps} numbered instructions"
            )

        elif numbered_steps >= 2:

            score += 1

            reason.append(
                f"{numbered_steps} numbered instructions"
            )

        # -------------------------
        # Multiple questions
        # -------------------------

        question_count = normalized_prompt.count("?")

        if question_count >= 3:

            score += 2

            reason.append(
                "Multiple questions"
            )

        elif question_count >= 2:

            score += 1

            reason.append(
                "More than one question"
            )

        # -------------------------
        # Constraints
        # -------------------------
        constraint_keyword = self._find_keywords(
            normalized_prompt,
            self.CONSTRAINT_KEYWORDS
        )

        if len(constraint_keyword) >= 3:
            score += 2

            reason.append(
                "Multiple Constraints"
            )
        elif len(constraint_keyword) >= 1:
            score += 1

            reason.append(
                "Contain constraints"
            )
        
        # final tier..
        if score >= 6:

            tier = "tier_3"

        elif score >= 3:

            tier = "tier_2"

        else:

            tier = "tier_1"

        return ComplexityResult(
            tier=tier,
            score=score,
            reasons=reason
        )

    def _find_keywords(
        self,
        text: str,
        keywords: list[str]
    ) -> list[str]:

        matches = []

        for keyword in keywords:

            if keyword in text:

                matches.append(
                    keyword
                )

        return matches