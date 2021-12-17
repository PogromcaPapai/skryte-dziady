TRANS = {
    'ó':'u',
    'ż':'rz',
    'ź':'zi',
    'ą':'om',
    'ś':'si',
    # 'ę':'en',
    'ń':'ni',
}
TRANS |= {i.capitalize():j.capitalize() for i,j in TRANS.items()}
TRANS |= {j:i for i,j in TRANS.items()}