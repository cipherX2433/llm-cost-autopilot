from app.router.complexity import ComplexityAnalyzer


def test_simple_prompt():

    analyzer = ComplexityAnalyzer()

    result = analyzer.analyze(
        "What is the capital of France?"
    )

    assert result.tier == "tier_1"


def test_moderate_prompt():

    analyzer = ComplexityAnalyzer()

    result = analyzer.analyze(
        "Summarize and analyze this customer review, compare and explain also"
    )

    assert result.tier == "tier_1"


def test_complex_prompt():

    analyzer = ComplexityAnalyzer()

    prompt = """
    Design a distributed system architecture for an
    e-commerce platform.

    Compare different approaches and explain the
    tradeoffs.

    Recommend the best architecture step by step.
    """

    result = analyzer.analyze(
        prompt
    )

    assert result.tier == "tier_3"