import csv
from ortools.sat.python import cp_model

# Create optimization model
model = cp_model.CpModel()

# Employees
employees = [
    "Ali",
    "Ahmed",
    "Saad",
    "Usman",
    "Hamza",
    "Bilal",
    "Zain",
    "Awais"
]

# Days
days = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

# Shifts
shifts = [
    "Morning",
    "Evening",
    "Night"
]

print("Employees:", len(employees))
print("Days:", len(days))
print("Shifts:", len(shifts))

# Calculate totals
total_shift_slots = len(days) * len(shifts) * 2
total_decision_variables = len(employees) * len(days) * len(shifts)

print("\nProject Statistics")
print("-" * 30)
print(f"Employees           : {len(employees)}")
print(f"Days                : {len(days)}")
print(f"Shifts Per Day      : {len(shifts)}")
print(f"Total Shift Slots   : {total_shift_slots}")
print(f"Decision Variables  : {total_decision_variables}")


# -----------------------------
# Decision Variables
# -----------------------------
work = {}

for e in employees:
    for d in days:
        for s in shifts:
            work[(e, d, s)] = model.NewBoolVar(f"work_{e}_{d}_{s}")

print(f"\nDecision Variables Created: {len(work)}")


# -----------------------------
# Constraint 1
# One employee can work only one shift per day
# -----------------------------

for e in employees:
    for d in days:
        model.Add(
            sum(work[(e, d, s)] for s in shifts) <= 1
        )

print("Constraint 1 Added Successfully")

# -----------------------------
# Constraint 2
# Each shift must have exactly 2 employees
# -----------------------------

for d in days:
    for s in shifts:
        model.Add(
            sum(work[(e, d, s)] for e in employees) == 2
        )

print("Constraint 2 Added Successfully")


# -----------------------------
# Constraint 3
# Fair workload
# -----------------------------

for e in employees:

    total_work = sum(
        work[(e, d, s)]
        for d in days
        for s in shifts
    )

    model.Add(total_work >= 5)
    model.Add(total_work <= 6)

print("Constraint 3 Added Successfully")


# -----------------------------
# Solve Model
# -----------------------------

solver = cp_model.CpSolver()

status = solver.Solve(model)


if status == cp_model.OPTIMAL:

    print("\n" + "=" * 50)
    print("EMPLOYEE SHIFT SCHEDULE")
    print("=" * 50)

    for d in days:

        print(f"\n{d}")

        for s in shifts:

            assigned = []

            for e in employees:

                if solver.Value(work[(e, d, s)]) == 1:
                    assigned.append(e)

            print(f"{s:<10}: {', '.join(assigned)}")

else:
    print("No Solution Found!")

print("\n")
print("=" * 50)
print("EMPLOYEE WORKLOAD")
print("=" * 50)

for e in employees:

    total = 0

    for d in days:
        for s in shifts:

            if solver.Value(work[(e, d, s)]) == 1:
                total += 1

    print(f"{e:<10} : {total} shifts")


    # -----------------------------
# Export Schedule to CSV
# -----------------------------

with open("employee_schedule.csv", "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow(["Day", "Shift", "Employee 1", "Employee 2"])

    for d in days:
        for s in shifts:

            assigned = []

            for e in employees:
                if solver.Value(work[(e, d, s)]) == 1:
                    assigned.append(e)

            writer.writerow([d, s, assigned[0], assigned[1]])

print("\nSchedule exported successfully to employee_schedule.csv")