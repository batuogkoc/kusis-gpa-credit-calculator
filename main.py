from input_txt import input_txt

letter_to_points = {
"A+":   4,
"A":    4,
"A-":   3.7,
"B+":   3.3,
"B":    3,
"B-":   2.7,
"C+":   2.3,
"C":    2,
"C-":   1.7,
"D+":   1.3,
"D":    1,
"F":    0,
"S":    None,
"U":    None,
"P":    None,
"W":    None,
}

if __name__ == "__main__":
    lines =  input_txt.strip().splitlines()
    classes = []
    for i in range(0, len(lines)-1, 13):
        curr_class = []
        for j in range(13):
            if j%2 == 0:
                curr_class.append(lines[i+j])
        classes.append(curr_class)
    
    total_credits = 0
    gpa = 0
    n=0

    for curr_class in classes:
        if curr_class[5] == "In Progress":
            continue
        n += 1
        letter_grade = curr_class[3]
        points = letter_to_points[letter_grade]
        curr_credits = float(curr_class[4].replace(",", "."))
        included_in_gpa = True if curr_class[6] == "Y" else False

        if included_in_gpa:
            total_credits += curr_credits
            gpa += points*curr_credits
    gpa /= total_credits

    print(f"Class count: {n}")
    print(total_credits)
    print(gpa)
    cred = 91 + 3*15
    # print((cred*4-3*0.3)/cred)