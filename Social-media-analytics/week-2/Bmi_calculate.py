# Underweight = <18.5
# Normal weight = 18.5–24.9
# Overweight = 25–29.9
# Obesity = BMI of 30 or greater
def check_bmi(bmi):
    if bmi < 18.5:
        return 'Underweight'
    elif 18.5 <= bmi <= 24.9:
        return 'Normal Weight'
    elif 25 <= bmi <= 29.9:
        return 'Overweight'
    else:
        return 'Obesity'


# data store format in hw.txt :
# 180 (person 1 height)
# 180 (person 1 weight)
# 170 (person 2 height)
# 200 (person 2 weight)

bmi_category_map = {}  # {key : value} = {bmi_category : List[bmi]}
with open('hw.txt', 'r') as bmi_data:
    content = [data.rstrip() for data in bmi_data.readlines()]
    a = 0
    for c in content:
        height = float(content[a]) / 100
        weight = float(content[a + 1]) / 2.2
        bmi = round(weight / (height ** 2), 2)

        bmi_category = check_bmi(bmi)
        category_list = bmi_category_map.get(bmi_category, [])
        a = a + 2
        category_list.append([bmi, int(a / 2)])
        bmi_category_map[bmi_category] = category_list
        if a >= len(content):
            break

for category, bmi_list in bmi_category_map.items():
    print("BMI Category : ", category)
    total_bmi = 0
    count = 0
    for bmi in bmi_list:
        total_bmi += bmi[0]
        print(f'Person-{bmi[1]} : {bmi[0]}')
        count += 1
    print('Average BMI : ', round(total_bmi / count, 2))


    # Function to classify BMI categories
    def check_bmi(bmi):
        if bmi < 18.5:
            return 'Underweight'
        elif 18.5 <= bmi <= 24.9:
            return 'Normal Weight'
        elif 25 <= bmi <= 29.9:
            return 'Overweight'
        else:
            return 'Obesity'


    # Dictionary to store BMI categories and corresponding BMIs
    bmi_category_map = {}

    # Read data from file
    with open('hw.txt', 'r') as bmi_data:
        content = [data.rstrip() for data in bmi_data.readlines()]  # Read and strip newline characters
        a = 0  # Initialize index
        while a < len(content):
            height = float(content[a]) / 100  # Convert height to meters
            weight = float(content[a + 1]) / 2.2  # Convert weight to kilograms
            bmi = round(weight / (height ** 2), 2)  # Calculate and round BMI

            bmi_category = check_bmi(bmi)  # Get BMI category
            category_list = bmi_category_map.get(bmi_category, [])  # Get or initialize list for category
            a += 2  # Move to next pair of values
            category_list.append([bmi, int(a / 2)])  # Append BMI and person index
            bmi_category_map[bmi_category] = category_list  # Update dictionary

    # Print BMI categories and corresponding BMIs
    for category, bmi_list in bmi_category_map.items():
        print("BMI Category:", category)
        total_bmi = 0
        count = 0
        for bmi in bmi_list:
            total_bmi += bmi[0]
            print(f'Person-{bmi[1]}: {bmi[0]}')
            count += 1
        print('Average BMI:', round(total_bmi / count, 2))

