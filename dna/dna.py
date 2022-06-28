import csv
import sys


def main():

    # TODO: Check for command-line usage

    if len(sys.argv) != 3:
        sys.exit('Usage: python dna.py data.csv sequence.txt')

    database_file = sys.argv[1]
    sequence_file = sys.argv[2]

    # TODO: Read database file into a variable
    database = dict()

    with open(database_file) as file:
        reader = csv.DictReader(file)
        strs = reader.fieldnames[1:]
        for person in reader:
            name = person['name']
            # separate name from the other keys in dictionary
            database[name] = {key: int(val) for (key, val) in person.items() if key != 'name'}

    # TODO: Read DNA sequence file into a variable
    with open(sequence_file) as file:
        sequence = file.read()

    # TODO: Find longest match of each STR in DNA sequence
    count = dict()
    for str in strs:
        count[str] = longest_match(sequence, str)

    # TODO: Check database for matching profiles
    for person, val in database.items():
        if val == count:
            return print(person)

    return print('No match')


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
