"""Simple one-off extraction of credit hour counts from Spring 24 CS class enrollments.

Sample row:
CS,110,Fluency with Info Tech,4.00 cr.,31281,45,100,1500-1550,mwf,282 LIL,Flores J,

SCH is credits * (capacity - available seats), or 4.0 * (100 - 45) in this example.
Because of labs we may have more than one entry for the same class.

"""

import csv
import sys

counts = {}

with open("data/enrollments-24S.csv", "r", newline="") as enrollments:
    reader = csv.reader(enrollments)
    for row in reader:
        try:
            dept_code = row[0]
            course_num = row[1]
            credits_text = row[3]
            credits,_ = credits_text.split()
            capacity = row[6]
            available = row[5]

            course_label = f"{dept_code} {course_num}"
            sch = int(float(credits)) * (int(capacity) - int(available))

            if course_label not in counts:
                counts[course_label] = 0
            counts[course_label] += sch

        except Exception as e:
            print(f"Rejected line: {row}", file=sys.stderr)
            print(e,file=sys.stderr)

print("SCH:")
for course, sch in counts.items():
    print(f"{course},{sch}")






