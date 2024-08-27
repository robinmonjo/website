import random

# source: https://cssgradient.io/gradient-backgrounds/

GRADIENTS = [
    """
    background-color: #4158D0;
    background-image: linear-gradient(43deg, #4158D0 0%, #C850C0 46%, #FFCC70 100%);
    """,
    """
    background-color: #0093E9;
    background-image: linear-gradient(160deg, #0093E9 0%, #80D0C7 100%);
    """,
    """
    background-color: #FBAB7E;
    background-image: linear-gradient(62deg, #FBAB7E 0%, #F7CE68 100%);
    """,
    """
    background-color: #FF9A8B;
    background-image: linear-gradient(90deg, #FF9A8B 0%, #FF6A88 55%, #FF99AC 100%);
    """,
    """
    background-color: #FFE53B;
    background-image: linear-gradient(147deg, #FFE53B 0%, #FF2525 74%);
    """,
    """
    background-color: #21D4FD;
    background-image: linear-gradient(19deg, #21D4FD 0%, #B721FF 100%);
    """,
    """
    background-color: #FBDA61;
    background-image: linear-gradient(45deg, #FBDA61 0%, #FF5ACD 100%);
    """,
    """
    background-color: #FA8BFF;
    background-image: linear-gradient(45deg, #FA8BFF 0%, #2BD2FF 52%, #2BFF88 90%);
    """,
    """
    background-color: #FAD961;
    background-image: linear-gradient(90deg, #FAD961 0%, #F76B1C 100%);
    """,
    """
    background-color: #FEE140;
    background-image: linear-gradient(90deg, #FEE140 0%, #FA709A 100%);
    """,
    """
    background-color: #1488CC;
    background: linear-gradient(to right, #2B32B2, #1488CC);
    """,
]


def random_gradient():
    return random.sample(GRADIENTS, 1)[0]
