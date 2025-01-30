    
def calculate_century(date_from, date_to):
    # Calculate centuries from date_from and date_to
    century_from = (date_from - 1) // 100 + 1
    century_to = (date_to - 1) // 100 + 1
    if century_from == century_to:
        century_label = f"{century_from}th century"
        centuries = [century_from]
    else:
        century_label = f"{century_from}th to {century_to}th century"
        centuries = range(century_from, century_to+1)
    return century_label, centuries