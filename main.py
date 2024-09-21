# from input_txt import input_txt
import argparse

LETTER_TO_POINTS = {
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

def parse_and_find_enrollment_group(file, credit_count):
    ret = {}
    with open(file, "r") as f:
        rows = [line.strip().split(";") for line in f.readlines()]
        enrollment_groups = rows[0][1:]
        for faculty, *credit_groups in rows[1:6]:
            ret[faculty] = None
            for idx, credit_group in enumerate(credit_groups):
                if credit_group == "":
                    continue
                low_range, high_range = credit_group.strip().split("-")
                
                if int(low_range) <= credit_count and credit_count <= int(high_range):
                    ret[faculty] = enrollment_groups[idx]
    
    return ret

if __name__ == "__main__":
    parser = argparse.ArgumentParser("This is a program that calculates your credits, GPA and enrollment group using your KUSIS 'Course History' tab")
    parser.add_argument("-f", "--file",
                        default="in.txt",
                        help="The input file that contains your copied and pasted KUSIS 'Course History' tab")
    parser.add_argument("-c", "--credit_file",
                        default="credit.csv",
                        help="The csv file that contains the credit groups. KEEP UP TO DATE!")
    args = parser.parse_args()

    with open(args.file, "r") as f:
        lines =  f.read().strip().splitlines()
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
            points = LETTER_TO_POINTS[letter_grade]
            curr_credits = float(curr_class[4].replace(",", "."))
            included_in_gpa = True if curr_class[6] == "Y" else False

            if included_in_gpa:
                total_credits += curr_credits
                gpa += points*curr_credits
        
        if total_credits == 0:
            print("Error, no classes specified, check your input file's integrity. Aborting!")
            exit(1)
        
        gpa /= total_credits


        print(f"Class Count: {n}")
        print(f"Total Credits: {total_credits}")
        print(f"GPA: {gpa}")
        print()
        print("-"*5 + "~Enrollment Groups~" + "-"*5)
        enrollment_groups = parse_and_find_enrollment_group(args.credit_file, total_credits)
        for faculty, group in enrollment_groups.items():
            if group is None:
                print(f"Note, problem when assigning group for {faculty}, check your files' integrities")
            else:
                print(f"{faculty}: {group}")