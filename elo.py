import math

# -----------------------------
# Configuration
# -----------------------------
BASE_ELO = 1000
K_FACTOR = 32

# -----------------------------
# Teams (9 teams total)
# -----------------------------
teams = {
    "4139D": BASE_ELO,
    "38657K": BASE_ELO,
    "52077X": BASE_ELO,
    "2989A": BASE_ELO,
    "4139E": BASE_ELO,
    "38657X": BASE_ELO,
    "44448A": BASE_ELO,
    "44110D": BASE_ELO,
    "4139F": BASE_ELO,
}

# -----------------------------
# Match data
# (A1, A2, A_score, B_score, B1, B2)
# -----------------------------

matches = [ ("4139D", "38657K", 31, 44, "52077X", "2989A"),
           ("4139E", "38657X", 103, 0, "44448A", "44110D"),
           ("4139F", "44448A", 20, 75, "4139D", "52077X"),
           ("38657K", "2989A", 55, 25, "4139F", "38657X"),
           ("52077X", "44110D", 85, 26, "4139E", "38657X"),
           ("4139F", "44110D", 57, 20, "38657K", "44448A"),
           ("4139E", "2989A", 28, 55, "4139D", "44110D"),
            ("52077X", "4139D", 77, 17, "2989A", "4139F"),
            ("38657X", "44448A", 73, 33, "4139E", "38657K"),
            ("44110D", "4139E", 0, 81, "2989A", "4139F"),
            ("38657K", "38657X", 69, 22, "4139D", "52077X"),
            ("44448A", "4139D", 76, 30, "44110D", "38657K"),
            ("2989A", "4139F", 47, 47, "4139E", "44448A"),
            ("52077X", "38657X", 57, 47, "2989A", "44110D"),
            ("52077X", "4139D", 56, 28, "38657X", "44448A"),
            ("38657K", "4139E", 55, 0, "4139F", "52077X"),
            ("4139D", "44110D", 83, 0, "4139E", "38657K"),
            ("44448A", "4139F", 22, 73, "38657X", "2989A"),
            ("2989A", "52077X", 69, 14, "4139E", "38657K"),
            ("4139F", "38657X", 12, 88, "4139D", "44110D"),
            ("44448A", "4139E", 33, 81, "38657X", "4139D"),
            ("44110D", "38657K", 42, 65, "52077X", "4139F"),
            ("2989A", "44448A", 44, 53, "38657K", "4139D"),
            ("44110D", "52077X", 24, 57, "44448A", "2989A"),
            ("4139F", "38657X", 10, 53, "4139E", "4139D"),

]

# -----------------------------
# Elo functions
# -----------------------------
def expected_score(rA, rB):
    return 1 / (1 + 10 ** ((rB - rA) / 400))

def margin_multiplier(scoreA, scoreB):
    margin = abs(scoreA - scoreB)
    return math.log(margin + 1, 10) + 1

# -----------------------------
# Process matches
# -----------------------------
def process_matches():
    for i, match in enumerate(matches, 1):
        A1, A2, scoreA, scoreB, B1, B2 = match

        ratingA = (teams[A1] + teams[A2]) / 2
        ratingB = (teams[B1] + teams[B2]) / 2

        expectedA = expected_score(ratingA, ratingB)
        expectedB = 1 - expectedA

        # Predicted winner
        if abs(expectedA - expectedB) < 1e-6:
            predicted = "Too close to call (50/50)"
        elif expectedA > expectedB:
            predicted = "Red Alliance"
        else:
            predicted = "Blue Alliance"


        # Actual result
        if scoreA > scoreB:
            actualA, actualB = 1, 0
            result = "Red Alliance wins"
        elif scoreB > scoreA:
            actualA, actualB = 0, 1
            result = "Blue Alliance wins"
        else:
            actualA, actualB = 0.5, 0.5
            result = "Draw"

        multiplier = margin_multiplier(scoreA, scoreB)

        deltaA = K_FACTOR * multiplier * (actualA - expectedA)
        deltaB = -deltaA

        teams[A1] += deltaA
        teams[A2] += deltaA
        teams[B1] += deltaB
        teams[B2] += deltaB

        print(f"Match {i}: {A1}/{A2} vs {B1}/{B2}")
        print(f"  Score: {scoreA} - {scoreB}")
        print(f"  Win Probability: Red Alliance = {expectedA*100:.1f}% | Blue Alliance = {expectedB*100:.1f}%")
        print(f"  Predicted Winner: {predicted}")
        print(f"  Actual Result: {result}")
        print(f"  Rating Change: {deltaA:.2f} / {deltaB:.2f}\n")

    # -----------------------------
    # Final rankings
    # -----------------------------
    print("\nFinal Elo Ratings:\n")
    for team, rating in sorted(teams.items(), key=lambda x: x[1], reverse=True):
        print(f"{team}: {rating:.1f}")

# -----------------------------
# Predict match
# -----------------------------
def predict_match():
    print("\n==== Custom Match Prediction ====")

    A1 = input("Red Alliance team 1: ").strip()
    A2 = input("Red Alliance team 2: ").strip()
    B1 = input("Blue Alliance team 1: ").strip()
    B2 = input("Blue Alliance team 2: ").strip()

    if A1 not in teams or A2 not in teams or B1 not in teams or B2 not in teams:
        print("Error: Unknown team.")
        return

    ratingA = (teams[A1] + teams[A2]) / 2
    ratingB = (teams[B1] + teams[B2]) / 2

    expectedA = expected_score(ratingA, ratingB)
    expectedB = 1 - expectedA

    if abs(expectedA - expectedB) < 1e-6:
        predicted = "Too close to call (50/50)"
    elif expectedA > expectedB:
        predicted = "Red Alliance"
    else:
        predicted = "Blue Alliance"

    print("\n==== Prediction Report ====")
    print(f"{A1} Elo: {round(teams[A1],1)}")
    print(f"{A2} Elo: {round(teams[A2],1)}")
    print(f"{B1} Elo: {round(teams[B1],1)}")
    print(f"{B2} Elo: {round(teams[B2],1)}")

    print(f"\nRed Alliance Elo: {round(ratingA,1)}")
    print(f"Blue Alliance Elo: {round(ratingB,1)}")

    print(f"\nWin probability:")
    print(f"Red Alliance: {expectedA*100:.1f}%")
    print(f"Blue Alliance: {expectedB*100:.1f}%")

    print(f"Prediction: {predicted}")
# -----------------------------
# Main loop
# -----------------------------

def main():
    while True:
        print("\n==== VEX Elo System ====")
        print("1) Process match history")
        print("2) Predict a custom matchup")
        print("3) Exit")

        choice = input("Select option: ").strip()

        if choice == "1":
            process_matches()
        elif choice == "2":
            process_matches()
            predict_match()
        elif choice == "3":
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()

