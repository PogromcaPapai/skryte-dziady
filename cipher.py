TRANS = {
    'ó':'u',
    # 'ż':'rz',
    # 'ź':'zi',
    # 'ą':'om',
    # 'ś':'si',
    # 'ę':'en'
}
TRANS |= {i.upper():j.upper() for i,j in TRANS.items()}
TRANS |= {j:i for i,j in TRANS.items()}